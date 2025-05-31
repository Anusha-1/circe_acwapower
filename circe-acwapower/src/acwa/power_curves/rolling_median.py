"""
acwa.power_curves.rolling_median

Generate a quick power curve as a rolling median
"""

import numpy as np
import pandas as pd

def create_fast_power_curve(
        df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create  fast power curve as a rolling median

    Args:
        df (pd.DataFrame): Data points speed, power

    Returns:
        pd.DataFrame: Power curve: bin, power, deviation
    """
    
    # Clean data
    df = df.dropna().copy()

    # Assign bin
    df["bin"] = df["speed"]\
        .apply(lambda x: round(x * 2) / 2)
    
    # Calculate median
    df = df.groupby(['bin']).agg({
        'power': 'median'
    }).reset_index()
    
    # Complete range dataframe
    bins = np.arange(0, 30.5, 0.5)
    df_comp = pd.DataFrame(data={'bin': bins})

    # Merge
    df = df_comp.merge(df, on='bin', how='left')

    # Interpolate
    df["power"] = df.apply(
        lambda row: 0 if row['bin'] <= 3 else max(0,row['power']),
        axis=1
    )
    df["power"] = df["power"].\
        interpolate(method="polynomial", order=2)\
        .ffill()
    
    # Empty deviation
    df["deviation"] = 0

    return df



