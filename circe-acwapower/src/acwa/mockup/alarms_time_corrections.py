"""
acwa.actions.alarms_time_correction

Apply time correction to create alarms real-time mockup
"""

from datetime import datetime
import logging
import pytz

import pandas as pd

from acwa.data import correct_future_times, transform_to_datetime, add_duration

def correct_alarm_times(
        df: pd.DataFrame, 
        current_year: datetime, 
        real_end_time: datetime,
        tz: pytz.BaseTzInfo
        ) -> pd.DataFrame:
    """
    Correct datetimes columns when creating real-time raw input alarms

    Args:
        df (pd.DataFrame): Dataframe with raw input data from static
        current_year (datetime): Current year (to correct data)
        real_end_time (datetime): Maximum datetime possible
        tz (pytz.BaseTzInfo): Timezone object

    Returns:
        pd.DataFrame: Corrected dataframe
    """

    datetime_cols = ["Detected", "Device ack.", "Reset/Run"]

    logging.info("Time corrections")       
    for col in datetime_cols:
        df = transform_to_datetime(
            df, 
            col, 
            "%Y-%m-%d %H:%M:%S.%f", 
            dest_col=col,
            new_year=current_year,
            drop_original_col=False
            )

    df = correct_future_times(
        df, 
        ["Device ack.", "Reset/Run"],
        ref_datetime=real_end_time,
        tz=tz)
    
    df = add_duration(
            df,
            "Detected",
            "Reset/Run",
            "Duration"
        )
    
    return df