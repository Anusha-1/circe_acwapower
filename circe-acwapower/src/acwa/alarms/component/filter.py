"""
acwa.alarms.component.filter

Module to filter alarms per turbine-component
"""

import pandas as pd

def filter_ongoing_alarms(
        df_all_alarms: pd.DataFrame, 
        df_status: pd.DataFrame,
        df_alarms_metadata: pd.DataFrame) -> pd.DataFrame:
    """
    Filter ongoing alarms per turbine and component

    Args:
        df_all_alarms (pd.DataFrame): Dataframe with all alarms
        df_status (pd.DataFrame): Status (will give us the last timestamp per turbine)
        df_alarms_metadata (pd.DataFrame): Alarms metadata

    Returns:
        pd.DataFrame: Dataframe with ongoing alarms 
    """

    # Merge alarms and status
    df_all_alarms = df_all_alarms.merge(
        df_status[["id_wtg_complete", "timestamp"]], 
        on="id_wtg_complete", 
        how="left"
    )

    # Condition for ongoing alarms
    ongoing = (
        df_all_alarms["timestamp"] > df_all_alarms["start_datetime"]
    ) & (df_all_alarms["end_datetime"].isna())

    # Filter
    df_current_alarms = df_all_alarms[ongoing]

    # Merge with metadata
    df_current_alarms = df_current_alarms.merge(
        df_alarms_metadata[['code', 'severity_scale', 'component']],
        on='code', how='left'
    )

    # Sort by severity_scale and timestamp
    df_current_alarms = df_current_alarms.sort_values(
        by=['severity_scale','timestamp']
    )

    return df_current_alarms
