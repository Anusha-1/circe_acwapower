"""
acwa.losses.performance

Module to calculate performance losses
"""

import pandas as pd

from acwa.db import run_query, read_table_as_df

from scipy.interpolate import PchipInterpolator


def calculate_performance_losses(df: pd.DataFrame, config_db: dict) -> pd.DataFrame:
    """
    Calculate performance losses

    Args:
        df (pd.DataFrame): DataFrame of datapoints
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with extra columns for performance losses
    """

    ## Load the power curves
    df_pc = run_query("select_all_power_curves", config_db, returns="Dataframe")
    df_wtg = read_table_as_df('wtg_config', config_db, 'vis')

    ## Loop in turbines
    lst_dfs = []
    lst_turbines = list(set(df["id_wtg_complete"]))
    for turb in lst_turbines:
        df_aux = df[df["id_wtg_complete"] == turb].copy()
        df_wtg_aux = df_wtg[df_wtg["id_wtg_complete"] == turb].copy()

        start = df_wtg_aux['wind_speed_start'].iloc[0]
        stop = df_wtg_aux['wind_speed_stop'].iloc[0]

        ## Performance loss to manufacturer reference
        df_aux_results_man = calculate_performance_losses_for_concept(
            df_aux, df_pc, "manufacturer", "MN", turb, 
            wind_start = start + 2, wind_stop = stop -1
        )

        ## Performance loss to historical reference
        df_aux_results_hist = calculate_performance_losses_for_concept(
            df_aux, df_pc, "Historical", "12 months", turb, 
            wind_start = start + 2, wind_stop = stop -1
        )

        ## Merge both
        df_aux_results = df_aux_results_man.merge(
            df_aux_results_hist[
                [
                    "id_wtg_complete",
                    "timestamp",
                    "historical_producible",
                    "historical_producible_min",
                    "historical_producible_max",
                    "historical_performance_loss",
                ]
            ],
            on=["id_wtg_complete", "timestamp"],
            how="left",
        )

        lst_dfs.append(df_aux_results)

    df = pd.concat(lst_dfs)

    ## Assign new code for underperforming 10-min
    min_ratio = 0.1 ## Minimum ratio loss/producible to be considered as "Underperforming"
    def __assign_underperforming_code(row):
        if (
            row["historical_performance_loss"] > min_ratio * row["historical_producible"]
            and row["manufacturer_performance_loss"] > min_ratio * row["manufacturer_producible"]
            and row["code"] == 0
        ):
            return -2
        else:
            return row["code"]

    df["code"] = df.apply(__assign_underperforming_code, axis=1)

    return df


def identify_power_curves(
    df_pc: pd.DataFrame, concept: str, period: str, id_wtg_complete: str
) -> pd.DataFrame:
    """
    Identifies all the power curves (with different densities and sectors)
    for a given turbine, concept and period

    Args:
        df_pc (pd.DataFrame): Power Curves dataframe
        concept (str): Concept
        period (str): Period
        id_wtg_complete (str): Turbine id

    Returns:
        pd.DataFrame: Dataframe with power curves
    """

    df_aux = df_pc[
        (df_pc["concept"] == concept)
        & (df_pc["period"] == period)
        & (df_pc["id_wtg_complete"] == id_wtg_complete)
    ].copy()
    return df_aux


def indentify_reference_density(df: pd.DataFrame, df_pc: pd.DataFrame) -> pd.DataFrame:
    """
    Identify reference density

    Args:
        df (pd.DataFrame): 10min data
        df_pc (pd.DataFrame): Power Curves

    Returns:
        pd.DataFrame: Dataframe with extra column 'density_for_correction'
    """

    df_pc_metadata = df_pc[["sector_name", "density"]].drop_duplicates().copy()

    ## Remove 'auto' and format to float
    df_pc_metadata = df_pc_metadata[df_pc_metadata["density"] != "auto"].copy()
    df_pc_metadata["density"] = df_pc_metadata["density"].astype("float")

    def __assign_density_for_correction(row):
        # Identify sector
        df_aux = df_pc_metadata[df_pc_metadata["sector_name"] == row["sector_name"]]
        dens_ref = list(df_aux["density"])
        if len(dens_ref) == 0:
            return None

        # List of distance to density
        distance = [abs(row["density"] - x) for x in dens_ref]
        zipped_list = zip(distance, dens_ref)
        min_pair = min(zipped_list, key=lambda x: x[0])
        density_for_correction = min_pair[1]

        return density_for_correction

    df["density_for_correction"] = df.apply(__assign_density_for_correction, axis=1)

    return df


def correct_to_reference_density(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct to reference density

    Args:
        df (pd.DataFrame): 10min data (with columns: 'wind_speed', 'density'
            and 'density_for_correction')

    Returns:
        pd.DataFrame: 10min data with extra column
            wind_speed_corrected_to_reference_density
    """

    df["wind_speed_corrected_to_reference_density"] = df["wind_speed"] * (
        df["density"] / df["density_for_correction"]
    ) ** (1 / 3)

    return df


def assign_reference_producible(
    df: pd.DataFrame, df_pc: pd.DataFrame, new_col: str, tolerance: float = 0.05
) -> pd.DataFrame:
    """
    Assign producible from reference (using the nearest density)

    Args:
        df (pd.DataFrame): 10min data
        df_pc (pd.DataFrame): Power Curves
        new_col (str): Column name for the producible
        tolerance (float, optional): Accepted tolerance for perfomance
            calculation, between 0 and 1. Defaults to 0.05 (i.e. 5%)

    Returns:
        pd.DataFrame: 10min data with extra columns for the producible +- X%
    """

    df_pc_metadata = df_pc[["sector_name", "density"]].drop_duplicates().copy()

    # Interpolation functions for each sector and density
    dict_interp_functions = dict()
    for i, row in df_pc_metadata.iterrows():
        df_pc_aux = df_pc[
            (df_pc["sector_name"] == row["sector_name"])
            & (df_pc["density"] == row["density"])
        ]

        dict_interp_functions[f"{row['sector_name']}-{row['density']}"] = (
            PchipInterpolator(df_pc_aux["bin"], df_pc_aux["power"])
        )

    # Interpolate
    def __interpolate_producible(row):
        if row["sector_name"] is None or pd.isna(row["density_for_correction"]):
            return None

        return dict_interp_functions[
            f"{row['sector_name']}-{row['density_for_correction']}"
        ](row["wind_speed_corrected_to_reference_density"])

    df[new_col] = df.apply(__interpolate_producible, axis=1).astype("float")
    df[f"{new_col}_min"] = df[new_col] * (1 - tolerance)
    df[f"{new_col}_min"] = df[f"{new_col}_min"].astype("float")
    df[f"{new_col}_max"] = df[new_col] * (1 + tolerance)
    df[f"{new_col}_max"] = df[f"{new_col}_max"].astype("float")

    return df


def calculate_performance_losses_for_turbine(
    df: pd.DataFrame, new_col: str, producible_col: str,
    wind_start: float, wind_stop: float
) -> pd.DataFrame:
    """
    Calculate performance losses for a turbine, having the producible columns

    Args:
        df (pd.DataFrame): 10min data
        new_col (str): Column for losses
        producible_col (str): Column for producible

    Returns:
        pd.DataFrame: 10min data with performance losses
    """

    def __calculate_performance_losses(row):

        if row['wind_speed'] < wind_start or row['wind_speed'] > wind_stop:
            return 0

        if row[f"{producible_col}"] > 0.1:

            if row["power"] > row[f"{producible_col}_max"]:
                return row[f"{producible_col}_max"] - row["power"]

            if row["power"] < row[f"{producible_col}_min"]:
                return row[f"{producible_col}_min"] - row["power"]

        return 0

    df[new_col] = df.apply(__calculate_performance_losses, axis=1)

    return df


def calculate_performance_losses_for_concept(
    df_aux: pd.DataFrame,
    df_pc: pd.DataFrame,
    concept: str,
    period: str,
    id_wtg_complete: str,
    wind_start: float = 0,
    wind_stop: float = 30,
) -> pd.DataFrame:
    """
    Calculate performance losses

    Args:
        df_aux (pd.DataFrame): Datapoints dataframe
        df_pc (pd.DataFrame): Power Curve dataframe
        concept (str): Power Curve concept to consider for reference.
        period (str): Power Curve period to consider as refernce.
        id_wtg_complete (str): Id of turbien
        wind_start (float, optional): Minimum wind speed to consider. 
            Defaults to 0.
        wind_stop (float, optional): Maximum wind speed to consider. 
            Defaults to 30.

    Returns:
        pd.DataFrame: Dataframe with extra columns with performance info
    """   


    df_pc_aux = identify_power_curves(df_pc, concept, period, id_wtg_complete)

    df_aux = indentify_reference_density(df_aux, df_pc_aux)

    df_aux = correct_to_reference_density(df_aux)

    df_aux = assign_reference_producible(
        df_aux, df_pc_aux, f"{concept.lower()}_producible"
    )

    df_aux = calculate_performance_losses_for_turbine(
        df_aux, 
        f"{concept.lower()}_performance_loss", 
        f"{concept.lower()}_producible",
        wind_start,
        wind_stop
    )

    df_aux = df_aux.drop(
        columns=["density_for_correction", "wind_speed_corrected_to_reference_density"]
    )

    return df_aux
