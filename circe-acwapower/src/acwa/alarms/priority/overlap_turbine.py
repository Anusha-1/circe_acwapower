"""
acwa.alarms.priority.overlap_turbine

Module to clean overlaps at specific turbine
"""

import pandas as pd

from acwa.alarms.priority.time_segments import extract_time_segments
from acwa.alarms.priority.main_alarm import assign_main_alarm
from acwa.alarms.priority.merge import merge_consecutive_alarms

def avoid_overlapping_alarms_in_turbine(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe with all the alarms corresponding to a specific turbine, 
    and cleans it by removing overlaps

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Corrected dataframe
    """

    df = df.reset_index()

    # Step 1: Extract time segments
    time_segments = extract_time_segments(df)
    
    # Step 2: Assign main alarm
    time_segments = assign_main_alarm(df, time_segments)
    
    # Step 3: Merge consecutive alarm
    df_segments = merge_consecutive_alarms(time_segments)

    # Step 4: Join with alarms info
    info_columns = list(df.columns)
    info_columns.remove("start_datetime")
    info_columns.remove("end_datetime")

    df_info = df[info_columns]
    final_df = df_segments.merge(
        df_info, how='left', left_on='main_alarm', right_on='index')
    final_df = final_df.drop(columns=['main_alarm', 'index'])
    final_df['duration'] = final_df.apply(
        lambda row: int((row['end_datetime'] - row['start_datetime']).total_seconds()),
        axis=1
    )

    if 'ongoing' in final_df.columns:
        final_df['ongoing'] = (final_df['ongoing']) & (final_df['end_datetime']==final_df['end_datetime'].max())

    return final_df
