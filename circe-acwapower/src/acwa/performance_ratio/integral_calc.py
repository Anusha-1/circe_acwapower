
import pandas as pd
import numpy as np


def calculate_area(df: pd.DataFrame,id:str,max_bin:float):
    """
    Calculate area under a power curve

    Args:
        df (pd.DataFrame): Dataframe with the power curves. Necesary columns:
            'pc_id', 'bin' and 'power'
        id (str): Id of the Power Curve to analyze. Has to match a value under
            the column 'pc_id'
        max_bin (float): Maximum bin to consider

    Returns:
        float: Area
    """

    df = df[df['pc_id']== id]
    df = df[df['bin']<= max_bin].reset_index()
    delta = df.loc[1,'bin'] - df.loc[0,'bin']
    return np.nansum(df['power']*delta)