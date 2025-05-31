"""
acwa.alarms.availability.production_formulas.user_II

Module with the formula to obtain User II Production-based Availability
"""

import pandas as pd


def obtain_production_user_II_availability(df_10min: pd.DataFrame) -> pd.DataFrame:
    """
    Obtain production-based availability User View II, according to norm

    Args:
        df_10min (pd.DataFrame): 10 min data

    Returns:
        pd.DataFrame: Dataframe with actual energy, potential energy and
            availability, per turbine and day

    """

    df_aux = df_10min.copy()

    # Remove or ignore losses and energy according to norm
    df_aux["loss"] = df_aux.apply(
        lambda row: pd.NA if row["priority"] in [5, 6, 11, 12] else row["loss"], 
        axis=1
    )
    df_aux["energy"] = df_aux.apply(
        lambda row: pd.NA if row["priority"] in [5, 6, 11, 12] else row["energy"],
        axis=1,
    )
    df_aux["loss"] = df_aux.apply(
        lambda row: 0 if row["priority"] in [1] else row["loss"], axis=1
    )

    # Group by
    df_agg = (
        df_aux.groupby(["id_wtg_complete", "day"])
        .agg({"energy": "sum", "loss": "sum"})
        .reset_index()
        .rename(columns={"energy": "actual_energy_user_II"})
    )
    df_agg["potential_energy_user_II"] = (
        df_agg["actual_energy_user_II"] + df_agg["loss"]
    )
    df_agg["production_user_II_availability"] = df_agg.apply(
        lambda row: row["actual_energy_user_II"] / row["potential_energy_user_II"] * 100
        if row["potential_energy_user_II"] > 0
        else 100,
        axis=1,
    )
    df_agg = df_agg.drop(columns="loss")

    df_agg['actual_energy_user_II'] = df_agg['actual_energy_user_II']\
        .astype('Float64')
    df_agg['potential_energy_user_II'] = df_agg['potential_energy_user_II']\
        .astype('Float64')
    df_agg['production_user_II_availability'] = df_agg['production_user_II_availability']\
        .astype('Float64')

    return df_agg