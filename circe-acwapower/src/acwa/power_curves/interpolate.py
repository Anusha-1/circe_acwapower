"""
acwa.power_curves.interpolate

Module to interpolate power curves for Power BI visualization
"""

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator 

def interpolate_power_curves(
        df_pc: pd.DataFrame, 
        df_pc_metadata: pd.DataFrame,
        resolution: float = 0.1
        ) -> pd.DataFrame:
    """
    Interpolate Power Curves to a lower resolution

    Args:
        df_pc (pd.DataFrame): Dataframe with power curves
        df_pc_metadata (pd.DataFrame): Dataframe with power curves metadata
        resolution (float, optional): Resolution of the interpolated curve in 
            m/s. Defaults to 0.1

    Returns:
        pd.DataFrame: Dataframe with interpolated curves
    """

    #assign id_wtg to each pc, and create final pc
    df_interpol = df_pc[['pc_id','bin','power','sigma']]
    lst_id = set(df_interpol['pc_id'])

    df_interpol.loc[:,'power'] = df_interpol.loc[:,'power'].fillna(0)   ##using .loc due to warning 
    df_interpol.loc[:,'sigma'] = df_interpol.loc[:,'sigma'].fillna(0)
    resampled_data = []

    for id in lst_id:
        df_subset = df_interpol[df_interpol['pc_id'] == id].sort_values(by='bin')
        
        # Create a new x range with 0.1 unit resolution
        x_new = np.arange(
            df_subset['bin'].min(), 
            df_subset['bin'].max()+resolution, 
            resolution)
        
        # Perform cubic spline interpolation
        cs = PchipInterpolator(df_subset['bin'], df_subset['power'])
        f_new = cs(x_new)
        cs2 = PchipInterpolator(df_subset['bin'], df_subset['sigma'])
        s_new = cs2(x_new)
        # Create a new DataFrame for the resampled data
        df_resampled = pd.DataFrame({
            'pc_id': id,
            'bin': x_new,
            'power': f_new,
            'sigma':s_new
        })
        
        # Append to the list
        resampled_data.append(df_resampled)
    
    df_resampled_combined = pd.concat(resampled_data, ignore_index=True)
    df_resampled_combined = pd.merge(
        df_resampled_combined,
        df_pc_metadata[['pc_id','id_wtg_complete','period', 'concept', 'sector_name', 'density']], 
        on= 'pc_id', 
        how= 'left')
    df_resampled_combined = df_resampled_combined.rename(
        columns= {'bin':'wind_speed'})
    
    return df_resampled_combined
