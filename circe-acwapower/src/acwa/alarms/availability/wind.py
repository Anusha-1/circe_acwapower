"""
acwa.alarms.availability.wind

Module for calculate daily wind time. We need this extra calculation before
running the wind availability formula
"""

from datetime import timedelta

import pandas as pd

def calculate_secs_with_wind_per_day(
    df_oper: pd.DataFrame, df_wtg: pd.DataFrame, df_daily: pd.DataFrame
):
    """
    Calculate number of seconds with wind per day and turbine

    Args:
        df_oper (pd.DataFrame): corresponds to oper_10min table
        df_wtg (pd.DataFrame): WTG_config
        df_daily: df to uptdate with time of wind availability
    """
    threshold_df = df_wtg[["id_wtg_complete", "wind_speed_start", "wind_speed_stop"]]
    df_oper = pd.merge(df_oper, threshold_df, on=["id_wtg_complete"], how="left")

    df_oper["wind_time_seconds"] = (
        df_oper["wind_speed"] > df_oper["wind_speed_start"]
    ) & (df_oper["wind_speed"] < df_oper["wind_speed_stop"])
    df_oper["wind_time_seconds"] = df_oper["wind_time_seconds"] * 600
       
    df_oper["day"] = df_oper["timestamp"].apply(
        lambda x: (x - timedelta(seconds=1)).date())
    ## We substract a delta because the timestamp always refers to the end of 
    ## the period. Thus, the timestamp 0:00 is the last of the previous day, not
    ## the first of the current date.

    df_aux = (
        df_oper.groupby(["id_wtg_complete", "day"])
        .agg({"wind_time_seconds": "sum"})
        .reset_index()
    )  # in 10minutals


    df_daily = pd.merge(df_daily, df_aux, on=["day", "id_wtg_complete"], how="left")

    return df_daily