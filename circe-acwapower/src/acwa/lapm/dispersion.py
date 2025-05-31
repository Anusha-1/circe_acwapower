"""
acwa.lapm.dispersion

Module to obtain dispersion by turbine, sector and wind speed
"""

import pandas as pd

def calculate_dispersion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates dispersion per turbine, sector and wind speed

    Args:
        df (pd.DataFrame): Dataframe of points. Needed columns: 
            'id_wtg_complete', 'sector_name', 'wind_speed_bin' and 'power

    Returns:
        pd.DataFrame: Grouped dataframe with statistics of power per turbine, 
            sector and wind speed
    """
    
    
    df_disp = df\
        .groupby(['id_wtg_complete', 'sector_name', 'wind_speed_bin'])\
        .agg(
            mean=('power', 'mean'),
            std=('power', 'std'),
            median=('power', lambda x: x.quantile(0.5)),
            q1 = ('power', lambda x: x.quantile(0.25)),
            q3 = ('power', lambda x: x.quantile(0.75))
        )\
        .reset_index()\
        .fillna(0)
    
    return df_disp
