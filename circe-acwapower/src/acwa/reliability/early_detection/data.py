"""
acwa.reliability.early_detection.data

Module to obtain the data to used for reliability early_detection
"""

from datetime import datetime

import pandas as pd

import acwa.config as conf
import acwa.db as db

def obtain_data_for_reliability_status(
        config_db: dict,
        min_timestamp: datetime,
        df_status: pd.DataFrame,
        id_wf: str) -> pd.DataFrame:
    """
    Obtain the reliability predictions that will be used to analyze the current
    reliability status of each turbine

    Args:
        config_db (dict): Database configuration
        min_timestamp (datetime): Minimum timestamp to consider
        df_status (pd.DataFrame): Status dataframe (incomplete)
        id_wf (str): WF id for wind farm to study

    Returns:
        pd.DataFrame: Reliability data to use.
    """

    ## Read reliability data from DB
    df_rel: pd.DataFrame = db.run_query(
        "select_status_reliability",
        config_db,
        params={"min_timestamp": min_timestamp},
        returns="Dataframe"
    )

    ## Filter data for current wind farm
    df_rel = df_rel.merge(
        df_status[['id_wtg_complete','id_wf']],
        on='id_wtg_complete')
    df_rel = df_rel[df_rel['id_wf']==id_wf]

    ## Filter datapoints to study (power > threshold)
    df_rel = df_rel[df_rel['power'] > conf.POWER_THRESHOLD*df_rel['nominal_power']]

    return df_rel
