"""
acwa.alarms.priority.main_alarm

Module to extract the main alarm
"""

from datetime import datetime

import pandas as pd

def assign_main_alarm(
        df: pd.DataFrame, 
        time_segments: list[dict[str, datetime]]
        ) -> list[dict[str, datetime | int]]:
    """
    Run through a list of time segments and assign the main alarm to it. If 
    there is no alarm for a time segment, remove it.

    Args:
        df (pd.DataFrame): Dataframe with the original alarms
        time_segments (list[dict[str, datetime]]): Time segments to study, i.e.
            List of dictionaries with keys "start_datetime" and "end_datetime" 
            and datetime objects as values

    Returns:
        list[dict[str, datetime | int]]: List of dictionaries with the time
            segment and an additional key "main_alarm" that contains the index
            of the alarm in the dataframe
    """

    filtered_segments = []
    for segment in time_segments:

        df_aux = df[(df['start_datetime'] < segment['end_datetime']) & (df['end_datetime'] > segment['start_datetime'])]
                
        if len(df_aux) > 0:
            segment["main_alarm"] = df_aux[df_aux['severity_scale'] == df_aux['severity_scale'].min()]\
                .sort_values(by="start_datetime")["index"].iloc[0]
            filtered_segments.append(segment)

    return filtered_segments