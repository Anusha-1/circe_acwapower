"""
acwa.alarms.availability.time_formulas.wind

Formula for wind availability
"""

import pandas as pd

def apply_wind_availability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the wind availability formula:

        wind_availability = (TCT - No wind) / TCT

    Args:
        df (pd.DataFrame): Dataframe with total time at each relevant group
            per day and turbine

    Returns:
        pd.DataFrame: Dataframe with extra columns for wind availability 
            info per day and turbine
    """


    # Obtain available time (num)
    df['wind_available_time'] = df['wind'].astype('int64')

    # Obtain total time (den)
    df['wind_total_time'] = (
        df[1]
        + df[2]
        + df[3]
        + df[4]
        + df[5]
        + df[6]
        + df[7]
        + df[8]
        + df[9]
        + df[10]
        + df[11]
    ) # Necessary to remove communication loss

    # Divide
    df['wind_availability'] = (df['wind_available_time'].astype(int) / df['wind_total_time'].astype(int) * 100).fillna(0)

    return df
