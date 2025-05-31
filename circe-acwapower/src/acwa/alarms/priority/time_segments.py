"""
acwa.alarms.priority.time_segments

Extract relevant time segments
"""

from datetime import datetime

import pandas as pd

def extract_time_segments(df: pd.DataFrame) -> list[dict[str, datetime]]:
    """
    Given a dataframe of alarms, extracts all the time segments that can be 
    obtained with consecutive timestamps from either the start or the end of the
    alarms.

    For instance if we have the alarms: [T1, T4], [T2, T8], [T3, T5], [T6, T7] 
    and [T9, T10], with T1 < T2 < ... < T10, the resulting ordered time segments
    are: [T1, T2], [T2, T3], [T3, T4], ... 

    Each one of these time segments can have one active alarm, several or none.

    Args:
        df (pd.DataFrame): Dataframe of alarms

    Returns:
        list[dict[str, datetime]]: List of dictionaries with keys 
            "start_datetime" and "end_datetime" and datetime objects as values
    """

    lst_times = list(set(df['start_datetime'])) + list(set(df['end_datetime']))
    lst_times.sort()

    lst_time_segments = []
    for i in range(len(lst_times) - 1):

        new_segment = {
            "start_datetime": lst_times[i],
            "end_datetime": lst_times[i+1],
        }

        if new_segment['start_datetime'] < new_segment['end_datetime']: 
            lst_time_segments.append(
                {
                    "start_datetime": lst_times[i],
                    "end_datetime": lst_times[i+1],

                }
            )

    return lst_time_segments
