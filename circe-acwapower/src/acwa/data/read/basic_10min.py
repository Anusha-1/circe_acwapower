"""
acwa.data.read_basic_10min

Module to read basic 10min data
"""

import pandas as pd

from acwa.data.datetime import transform_to_datetime
from acwa.db import run_query, read_table_as_df


def read_basic_10min_data(incremental: bool, config_db: dict) -> pd.DataFrame:
    """
    Read basic 10 min data

    Args:
        incremental (bool): If True, only reads data that has not been processed
            in oper_10min
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with 10-min data
    """

    if incremental:
        df: pd.DataFrame = run_query(
            "select_incremental_10min_basic",
            config_db,
            returns="Dataframe"
        )
    else:
        df = read_table_as_df(
            "basic_10min",
            config_db,
            "intermediate"
        )

    # Formatting
    df['angle_deviation_sign'] = df['angle_deviation_sign'].astype("Int64")

    if config_db['type'] == 'SQLite':
        df = transform_to_datetime(
            df, 
            "timestamp", 
            "%Y-%m-%d %H:%M:%S.%f", 
            "timestamp", 
            drop_original_col=False)

    return df
