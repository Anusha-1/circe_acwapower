"""
acwa.reliability.early_detection.period

Define the period to study for reliability status
"""

from datetime import datetime

import pandas as pd

import acwa.config as conf

def obtain_min_timestamp_for_reliability_status(
        df_status: pd.DataFrame,
) -> datetime:
    """
    Obtain the minimum timestamp for the study of recent temperature signals,
    in order to obtain current reliability status per turbine

    Args:
        df_status (pd.DataFrame): Current status dataframe of turbines belonging
            to a specific wind farm.

    Returns:
        datetime: Datetime from which we retrieve reliability data for its study
    """

    ## Extract timestamp. We are assuming here that we have only one wind farm,
    ## and thus, the timestamp are expected to be the same for each WTG. 
    ## However, we are not checking this and taking the minimum.
    last_timestamp = df_status['timestamp'].min()

    if isinstance(last_timestamp, str):
        last_timestamp = datetime.strptime(
            last_timestamp, "%Y-%m-%d %H:%M:%S.%f")

    ## From the current timestamp, we substract a timedelta with the period of
    ## study
    min_timestamp = last_timestamp - conf.EARLY_DETECTION_PERIOD

    return min_timestamp
