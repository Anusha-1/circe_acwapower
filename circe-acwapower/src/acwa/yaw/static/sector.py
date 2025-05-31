"""
acwa.yaw.angle_deviation.sector

Module to discretize angle deviation into sectors
"""

import pandas as pd

def assign_angle_deviation_sector(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a discretized sector to 'angle_deviation'

    Args:
        df (pd.DataFrame): Dataframe with column 'angle_deviation'

    Returns:
        pd.DataFrame: Dataframe with extra column 'angle_deviation_sector'
    """

    def __assign_angle_deviation_sector(x):

        if pd.isna(x):
            return None

        if 0 < x <= 5:
            return "0 to 5"
        if 5 < x <= 10:
            return "5 to 10"
        if 10 < x <= 15:
            return "10 to 15"
        if 15 < x <= 20:
            return "15 to 20"
        if 20 < x <= 25:
            return "20 to 25"
        if 25 < x <= 30:
            return "25 to 30"
        if 30 < x <= 50:
            return "30 to 50"
        if 50 < x <= 70:
            return "50 to 70"
        if 70 < x <= 90:
            return "70 to 90"
        if 90 < x <= 110:
            return "90 to 110"
        if 110 < x <= 180:
            return "110 to 180"
        
        if -5 < x <= 0:
            return "0 to -5"
        if -10 < x <= -5:
            return "-5 to -10"
        if -15 < x <= -10:
            return "-10 to -15"
        if -20 < x <= -15:
            return "-15 to -20"
        if -25 < x <= -20:
            return "-20 to -25"
        if -30 < x <= -25:
            return "-25 to -30"
        if -50 < x <= -30:
            return "-30 to -50"
        if -70 < x <= -50:
            return "-50 to -70"
        if -90 < x <= -70:
            return "-70 to -90"
        if -110 < x <= -90:
            return "-90 to -110"
        if -180 < x <= -110:
            return "-110 to -180"
        
        return None #This shouldnt happen
    
    df['angle_deviation_sector'] = df['angle_deviation'].apply(
        __assign_angle_deviation_sector)

    return df
