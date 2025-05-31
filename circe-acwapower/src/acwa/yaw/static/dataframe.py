"""
acwa.yaw.angle_deviation.dataframe

Module to assign angle deviation in a dataframe
"""

import pandas as pd

from acwa.yaw.static.row import calculate_angle_deviation_in_row

def calculate_angle_deviation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate angle deviation.

    Args:
        df (pd.DataFrame): Dataframe with columns 'wind_direction' and 
            'nacelle_direction'

    Returns:
        pd.DataFrame: Dataframe with extra column 'angle_deviation' as the 
            differente between wind and nacelle direction
    """

    df['angle_deviation'] = df.apply(calculate_angle_deviation_in_row, axis=1)

    return df
