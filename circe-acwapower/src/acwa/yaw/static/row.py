"""
acwa.yaw.angle_deviation.row

Row function to calculate angle deviation
"""

import pandas as pd

def calculate_angle_deviation_in_row(row: pd.Series) -> float:
    """
    Calculate angle deviation in a row

    Args:
        row (pd.Series): Row in a dataframe with fields: "wind_direction" and 
            "nacelle_direction"

    Returns:
        float: Difference between wind and nacelle direction
    """

    if pd.isna(row['wind_direction']) or pd.isna(row['wind_direction']):
        return None 

    diff = row['wind_direction'] - row['nacelle_direction']

    if diff > 180:
        diff -= 360
    elif diff <= -180:
        diff += 360

    return diff
