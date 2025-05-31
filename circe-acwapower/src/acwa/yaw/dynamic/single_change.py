"""
acwa.yaw.dynamic.single_change

Compare a direction with the previous instant and determine if it is considered
a change
"""

import numpy as np
import pandas as pd

def mark_single_directional_change(
        row: pd.Series, col_now: str, col_prev: str, threshold: float) -> bool:
    """
    Mark with a boolean if there is a directional change in a specific row

    Args:
        row (pd.Series): Row of a dataframe
        col_now (str): Name of the column with the current direction
        col_prev (str): Name of the column with the previous direction 
            (typically a shift of the col_now column)
        threshold (float): Threshold to be considered a change

    Returns:
        bool: True if the direction difference is large enough to be considered
            a change
    """
      
    dir1 = row[col_now]
    dir2 = row[col_prev]

    if np.isnan(dir1) or np.isnan(dir2):
        return False
    
    ## Change in 0-360
    diff1 = abs(dir1 - dir2)

    ## Change in -180 - 180
    if dir1 > 180:
        dir1 -= 360
    if dir2 > 160:
        dir2 -= 360

    diff2 = abs(dir1 - dir2)

    return min(diff1, diff2) > threshold
