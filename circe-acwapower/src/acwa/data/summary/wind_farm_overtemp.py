"""
acwa.data.summary.wind_farm_overtemp

Module to add overtemperature KPIs at wind farm level
"""

import pandas as pd

from acwa.db import read_table_as_df

def add_overtemperature_to_kpis(
    config_db: dict, 
    df_wtg_config: pd.DataFrame,
    df_kpis: pd.DataFrame
) -> pd.DataFrame:
    """
    Add overtemperature to KPIs

    Args:
        config_db (dict): Database configuration
        df_wtg_config (pd.DataFrame): Dataframe with WTG metadata
        df_kpis (pd.DataFrame): Previous KPIs results
        
    Returns:
        pd.DataFrame: KPI results with extra column for overtemperature
    """

    # Read reliability predictions
    df_reliability_ts = read_table_as_df("reliability_ts", config_db, "intermediate")

    # Identify over-temperature columns
    df_temp_signals = read_table_as_df("temperature_signals", config_db, "vis")
    lst_over_signals = [
        f"{x}_over" for x in df_temp_signals["name_in_origin"].to_list()
    ]

    # Format data as boolean matrix
    id_columns = ["id_wtg_complete", "timestamp"]
    df_rel = (
        df_reliability_ts[id_columns + lst_over_signals].set_index(id_columns).copy()
    )

    # Sum overtemperature signals
    df_rel["sum_over"] = df_rel.sum(axis=1)

    # Obtain data availability (by counting predictions)
    lst_median_signals = [
        f"{x}_median" for x in df_temp_signals["name_in_origin"].to_list()
    ]
    df_rel_aux = (
        df_reliability_ts[id_columns + lst_median_signals].set_index(id_columns).copy()
    )
    df_rel["ok_data"] = df_rel_aux.count(axis=1)  # It ignores NaN

    # Group by id_wtg_complete and period (year - month)
    df_rel = df_rel[["sum_over", "ok_data"]].reset_index().copy()
    df_rel["year"] = df_rel["timestamp"].dt.strftime("%Y")
    df_rel["month"] = df_rel["timestamp"].dt.strftime("%B")
    df_rel_group = (
        df_rel[["id_wtg_complete", "year", "month", "sum_over", "ok_data"]]
        .groupby(["id_wtg_complete", "year", "month"])
        .sum()
    )

    # Group by wind farm (monthly)
    df_rel_group = (
        df_rel_group[["sum_over", "ok_data"]]
        .reset_index()
        .merge(df_wtg_config[["id_wtg_complete", "id_wf"]], on="id_wtg_complete")
        .drop(columns=["id_wtg_complete"])
    )
    df_rel_group_month = df_rel_group.groupby(["id_wf", "month", "year"]).sum()
    df_rel_group_month["overtemperature_percentage"] = (
        df_rel_group_month["sum_over"] / df_rel_group_month["ok_data"] * 100
    )

    # Group by wind farm (year)
    df_rel_group_year = (
        df_rel_group_month[["sum_over", "ok_data"]]
        .reset_index()
        .groupby(["id_wf", "year"])
        .sum()
    )
    df_rel_group_year["overtemperature_percentage"] = (
        df_rel_group_year["sum_over"] / df_rel_group_year["ok_data"] * 100
    )
    df_rel_group_year["month"] = "All"

    # Group by general months
    df_rel_group_general_month = (
        df_rel_group_month[["sum_over", "ok_data"]]
        .reset_index()
        .groupby(["id_wf", "month"])
        .sum()
    )
    df_rel_group_general_month["overtemperature_percentage"] = (
        df_rel_group_general_month["sum_over"] / df_rel_group_general_month["ok_data"] * 100
    )
    df_rel_group_general_month["year"] = "All"

    # Group by all
    df_rel_group_all = (
        df_rel_group_month[["sum_over", "ok_data"]]
        .reset_index()
        .groupby(["id_wf"])
        .sum()
    )
    df_rel_group_all["overtemperature_percentage"] = (
        df_rel_group_all["sum_over"] / df_rel_group_all["ok_data"] * 100
    )
    df_rel_group_all["year"] = "All"
    df_rel_group_all["month"] = "All"

    # Concat
    df_rel = pd.concat([
        df_rel_group_month['overtemperature_percentage'].reset_index(), 
        df_rel_group_year[['overtemperature_percentage', 'month']].reset_index(),
        df_rel_group_general_month[['overtemperature_percentage', 'year']].reset_index(),
        df_rel_group_all[['overtemperature_percentage', 'year', 'month']].reset_index()],
        ignore_index=True)
    
    # Merge
    df_kpis = df_kpis.merge(df_rel, on=['id_wf','year','month'])
    
    return df_kpis
