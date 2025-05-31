"""
acwa.report.table_alarms

Table for alarms
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from acwa.db import read_table_as_df
from acwa.data import extract_summary_alarms


def create_table_alarms(
        id_wf: str, 
        date: datetime, 
        config: dict, 
        max_alarms: int = None) -> pd.DataFrame:
    """
    Create the table of alarms

    Args:
        id_wf (int): Id of wind farm
        date (datetime): Threshold date
        config (dict): Configuration
        max_alarms (int, optional): Number of maximum alarms to consider. 
            Defaults to None

    Returns:
        pd.DataFrame: Table of alarms
    """

    # Read data
    df_meta = read_table_as_df("alarms_metadata", config["db"], "vis")
    df_alarms_1day = read_table_as_df("treated_events_1day", config["db"], "vis")

    # Filter data for report
    last_day = date + relativedelta(days=1)
    df_alarms_1day = df_alarms_1day[df_alarms_1day['day'] < last_day]

    df_alarms_summ = extract_summary_alarms(df_alarms_1day)
    df_alarms_summ = df_alarms_summ.merge(
        df_meta[["code", "description"]], on="code", how="left"
    )

    # Filter daily alarms
    df_alarms_1day = df_alarms_1day[
        (df_alarms_1day["day"] == date) & (df_alarms_1day["id_wf"] == id_wf)
    ]

    # Group by code
    df_alarms_1day_group = (
        df_alarms_1day.groupby(["code"])
        .agg(duration=("duration", "sum"), losses=("losses", "sum"))
        .sort_values(by="losses", ascending=False)
        .reset_index()
        .merge(df_meta[["code", "description"]], on="code", how="left")
    )

    # Turbines affected by code
    affected_turbines = {}
    for code in set(df_alarms_1day_group["code"]):
        df_aux = df_alarms_1day[df_alarms_1day["code"] == code]
        affected_turbines[code] = ", ".join(df_aux["id_wtg"].to_list()) + ": "
    df_alarms_1day_group["full_description"] = (
        df_alarms_1day_group["code"].apply(lambda x: affected_turbines[x])
        + df_alarms_1day_group["description"]
    )

    # Obtain monthly alarms
    month = date.strftime("%B")
    year = date.strftime("%Y")
    df_alarms_month = df_alarms_summ[
        (df_alarms_summ["month"] == month)
        & (df_alarms_summ["year"] == year)
        & (df_alarms_summ["id_wf"] == id_wf)
        & (df_alarms_summ['id_wtg_complete'] == 'All')
        & (df_alarms_summ['code'].isin(affected_turbines.keys()))
    ]    
    df_alarms_1day_group = df_alarms_1day_group.merge(
        df_alarms_month[['code','total_losses']], on='code', how='left'
    ).rename(columns={'total_losses': 'monthly_losses'})

    # Obtain yearly alarms
    df_alarms_year = df_alarms_summ[
        (df_alarms_summ["month"] == "All")
        & (df_alarms_summ["year"] == year)
        & (df_alarms_summ["id_wf"] == id_wf)
        & (df_alarms_summ['id_wtg_complete'] == 'All')
        & (df_alarms_summ['code'].isin(affected_turbines.keys()))
    ]    
    df_alarms_1day_group = df_alarms_1day_group.merge(
        df_alarms_year[['code','total_losses']], on='code', how='left'
    ).rename(columns={'total_losses': 'yearly_losses'})

    # Reformat and reorder
    df_alarms_1day_group["duration"] = df_alarms_1day_group["duration"] / 3600.0
    df_alarms_1day_group["losses"] = df_alarms_1day_group["losses"] / 1000.0
    df_alarms_1day_group["monthly_losses"] = df_alarms_1day_group["monthly_losses"] / 1000.0
    df_alarms_1day_group["yearly_losses"] = df_alarms_1day_group["yearly_losses"] / 1000.0
    df_alarms_1day_group = df_alarms_1day_group[
        ["full_description", "duration", "losses", "monthly_losses", "yearly_losses"]
    ]
    df_alarms_1day_group = df_alarms_1day_group.set_index("full_description")

    # Limit alarms
    if max_alarms is not None:
        df_alarms_1day_group = df_alarms_1day_group.head(max_alarms)

    # Sum total
    df_alarms_1day_group.loc["Total"] = df_alarms_1day_group.sum(axis=0)
    df_alarms_1day_group = df_alarms_1day_group.round(2).astype(str)

    return df_alarms_1day_group
