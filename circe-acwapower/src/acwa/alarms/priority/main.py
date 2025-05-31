"""
acwa.alarms.priority.main

Main module to obtain priority alarms
"""

from datetime import datetime
import logging

import pandas as pd

from acwa.db import run_query
from acwa.data import extract_alarms_temporal_horizon_basic, transform_to_datetime
from acwa.alarms.priority.overlap_all import avoid_overlapping_alarms

def obtain_priority_alarms(now: datetime, config_db: dict, incremental: bool):
    """
    Obtain priority alarms

    Args:
        now (datetime): Datetime object with the temporal horizon to consider.
        config_db (dict): Configuration for database
        incremental (bool): If True, loads only the last alarms

    Returns:
        pd.DataFrame: Dataframe with alarms
    """

    logging.info("Reading alarms and join with metadata")
    if incremental:
        extract_alarms_temporal_horizon_basic(config_db)
        df_alarms: pd.DataFrame = run_query(
            "select_incremental_alarms",
            config_db,
            returns='Dataframe'
        )
    else:
        df_alarms: pd.DataFrame = run_query(
            "join_alarms_and_metadata",
            config_db,
            returns="Dataframe")
    
    if config_db['type'] == 'SQLite':
        df_alarms = transform_to_datetime(
            df_alarms, "start_datetime", "%Y-%m-%d %H:%M:%S.%f", "start_datetime", drop_original_col=False)
        df_alarms = transform_to_datetime(
            df_alarms, "end_datetime", "%Y-%m-%d %H:%M:%S.%f", "end_datetime", drop_original_col=False)

    df_alarms['ongoing'] = None
    df_alarms['duration'] = None
    if len(df_alarms) > 0:
        logging.info("Format")
        df_alarms['ongoing'] = df_alarms['end_datetime'].apply(
            lambda x: True if pd.isnull(x) else False
        )
        df_alarms['end_datetime'] = df_alarms['end_datetime'].apply(
            lambda x: now if pd.isnull(x) else x
        )
        df_alarms['duration'] = df_alarms.apply(
            lambda row: int((row['end_datetime'] - row['start_datetime']).total_seconds()),
            axis=1
        )

        logging.info("Avoid overlapping alarms")
        df_alarms = avoid_overlapping_alarms(df_alarms)

        logging.info("Formatting")
        df_alarms['severity_scale'] = df_alarms['severity_scale'].astype("Int64")

    return df_alarms
    