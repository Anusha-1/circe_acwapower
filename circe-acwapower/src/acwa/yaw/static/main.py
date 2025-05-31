"""
acwa.yaw.static

Module to perform the whole yaw static analysis
"""

import pandas as pd


from acwa.yaw.static.dataframe import calculate_angle_deviation
from acwa.yaw.static.sector import assign_angle_deviation_sector
from acwa.yaw.static.sign import assign_angle_deviation_sign_flag

def calculate_yaw_static_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the necessary variables for yaw static analysis

    Args:
        df (pd.DataFrame): Dataframe with operational data points (10min or 1min)

    Returns:
        pd.DataFrame: Dataframe with extra columns with yaw static variables
    """

    df = calculate_angle_deviation(df)

    df = assign_angle_deviation_sector(df)

    df = assign_angle_deviation_sign_flag(df)

    return df
