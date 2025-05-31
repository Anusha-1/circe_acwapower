"""
acwa.alarms.priority.merge

Module to merge consecutive alarms
"""

from datetime import datetime

import pandas as pd

def merge_consecutive_alarms(
        time_segments: list[dict[str, datetime | int]]) -> pd.DataFrame:
    """
    Run through a dictionary of time segments with main alarm, and merge them if 
    they correspond to the same main alarm, modifying the time boundaries

    Args:
        time_segments (list[dict[str, datetime | int]]): Dictionary of time 
            segments, including the keys:

            - "start_datetime"
            - "end_datetime"
            - "main_alarm"

    Returns:
        pd.DataFrame: Dataframe with resulting alarms. There shouldn't be 
            overlapping alarms or consecutive alarms that are referred to the 
            same alarm index
    """

    current_segment = time_segments[0]
    new_segments = []

    for segment in time_segments[1:]:

        if current_segment['main_alarm'] == segment['main_alarm']:
            current_segment['end_datetime'] = segment['end_datetime']

        else:
            new_segments.append(current_segment)
            current_segment = segment

    new_segments.append(current_segment)

    return pd.DataFrame.from_records(new_segments)
