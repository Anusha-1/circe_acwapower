"""
acwa.data.basic_alarms

Module to read basic 10min data
"""

import pandas as pd

from acwa.db import run_query, read_table_as_df
from acwa.data.horizon import extract_alarms_temporal_horizon


def read_basic_alarms(incremental: bool, config_db: dict) -> pd.DataFrame:
    """
    Read basic alarms

    Args:
        incremental (bool): If True, only reads data that has not been processed
            in oper_10min
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with 10-min data
    """

    if incremental:
        extract_alarms_temporal_horizon(config_db)
        df: pd.DataFrame = run_query(
            "select_incremental_alarms_basic",
            config_db,
            returns="Dataframe"
        )
    else:
        df = read_table_as_df(
            "basic_alarms",
            config_db,
            "intermediate"
        )

    # Format start and end datetimes as datetime objects
    df['start_datetime'] = pd.to_datetime(df['start_datetime'])
    df['end_datetime'] = pd.to_datetime(df['end_datetime'])


    return df
