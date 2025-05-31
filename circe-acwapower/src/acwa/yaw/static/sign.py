"""
acwa.yaw.angle_deviation.sign

Assign a sign flag to angle deviation
"""

import pandas as pd

def assign_angle_deviation_sign_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a sign flag for angle deviation (+1 if angle deviation is positive,
    -1 otherwise)

    Args:
        df (pd.DataFrame): Dataframe with column angle deviation

    Returns:
        pd.DataFrame: Dataframe with extra column 'angle_deviation_sign'
    """

    df['angle_deviation_sign'] = -1 + 2 * (df['angle_deviation'] > 0)
    df.loc[df['angle_deviation'].isna(), 'angle_deviation_sign'] = None
    df['angle_deviation_sign'] = df['angle_deviation_sign'].astype("Int32")

    return df
