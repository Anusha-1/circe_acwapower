"""
acwa.alarms.join.min_1.all

Module to join all the 1 min data with alarms
"""

import pandas as pd


def join_alarms_and_1min_data(
    df_1min: pd.DataFrame, df_alarms: pd.DataFrame
) -> pd.DataFrame:
    """
    Joins alarms and 1min data.

    NOTE: This same function could be used for 10min data as well. But we 
    decided to use the wod package instead. Maybe it would be better to unify 
    all.

    Args:
        df_1min (pd.DataFrame): 1min data
        df_alarms (pd.DataFrame): Alarms

    Returns:
        pd.DataFrame: 1min data with extra column 'code', corresponding to the 
            alarm running at that moment (or 0 if none)
    """

    # Sort dataframes
    df_1min = df_1min.sort_values(by="timestamp")
    df_alarms = df_alarms.sort_values(by="start_datetime")

    # Merge asof. Merges 1 min data with previos alarm
    df_merged = pd.merge_asof(
        df_1min,
        df_alarms[['id_wtg_complete', 'code', 'start_datetime', 'end_datetime']],
        by="id_wtg_complete",
        left_on="timestamp",
        right_on="start_datetime",
        direction="backward",
    )
    
    # Filter out the 'code' value if it is not inside the ranges
    df_merged["code"] = df_merged.apply(
        lambda row: row["code"]
        if row["start_datetime"] <= row["timestamp"] <= row["end_datetime"]
        else 0,
        axis=1,
    ).astype("Int64")
    df_merged = df_merged[list(df_1min.columns) + ['code']]

    return df_merged
