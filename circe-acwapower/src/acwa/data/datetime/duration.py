"""
acwa.data.datetime.duration

Module to calculate duration
"""

from datetime import datetime

import pandas as pd

from acwa.data.datetime.format import format_timedelta_to_HHMMSS

def add_duration(
        df: pd.DataFrame,
        start_col: str,
        end_col: str,
        dest_col: str
) -> pd.DataFrame:
    """
    Adds a duration column (as the difference between an end datetime column and
    a start datetime column)

    Args:
        df (pd.DataFrame): Dataframe
        start_col (str): Column with start datetime
        end_col (str): Column with end datetime
        dest_col (str): Column where to place the duration

    Returns:
        pd.DataFrame: Dataframe with duration
    """
    
    def __add_duration(row):
        if isinstance(row[end_col], datetime) and isinstance(row[start_col], datetime):
            delta = row[end_col] - row[start_col]
            try:
                return format_timedelta_to_HHMMSS(delta)
            except Exception:
                return "Ongoing" # We should fix this better...
        else:
            return "Ongoing"

    df[dest_col] = df.apply(__add_duration, axis=1)

    return df 
