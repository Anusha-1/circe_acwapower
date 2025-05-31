"""
acwa.alarms.stats.past_turbines

Module to complete alarms information from previous alarms, at a particular
turbine
"""

import numpy as np
import pandas as pd

def add_past_times(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the final form of a dataframe with priority alarms (for a specific
    turbine) and calculates:
        - time_since_previous_alarm: Time (in seconds) from the start of the current 
            alarm to the end of the next one (of whatever code)
        - time_since_previous_same_alarm: Time (in seconds) from the start of the 
            current alarm to the end of the previous alarm of the same code

    Args:
        df (pd.DataFrame): Dataframe of priority alarms

    Returns:
        pd.DataFrame: Dataframe with the extra columns
    """

    lst_time_since_previous = []
    lst_time_since_previous_same = []

    for i, row in df.iterrows():

        if i == 0:
            lst_time_since_previous.append(np.nan)
            lst_time_since_previous_same.append(np.nan)
            continue

        current_start = row['start_datetime']

        lst_time_since_previous.append(
            (current_start - df.iloc[i-1]['end_datetime']).total_seconds()
        )

        df_aux = df[(df['code'] == row['code']) & (df['end_datetime'] < current_start)]

        if len(df_aux) > 0:
            lst_time_since_previous_same.append(
                (current_start - df_aux.iloc[-1]['end_datetime']).total_seconds()
            )
        else:
            lst_time_since_previous_same.append(np.nan)

    df['time_since_previous_alarm'] = lst_time_since_previous
    df['time_since_previous_same_alarm'] = lst_time_since_previous_same

    df['time_since_previous_alarm'] = np.floor(
        pd.to_numeric(
            df['time_since_previous_alarm'], 
            errors='coerce')).astype('Int64')
    df['time_since_previous_same_alarm'] = np.floor(
        pd.to_numeric(
            df['time_since_previous_same_alarm'], 
            errors='coerce')).astype('Int64')

    return df
