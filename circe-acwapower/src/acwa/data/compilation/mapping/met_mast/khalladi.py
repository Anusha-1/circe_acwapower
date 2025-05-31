"""
acwa.data.compilation.mapping.met_mast.khalladi

Mapping function for Khalladi Met Mast
"""

import logging

import numpy as np
import pandas as pd

def map_met_mast_Khalladi(
        df: pd.DataFrame,
        id_mm: str,
        df_map: pd.DataFrame,
        wf_name: str
) -> pd.DataFrame:
    """
    Map Met Mast variables with Khalladi format

    Args:
        df (pd.DataFrame): Input dataframe
        id_mm (str): Met Mast ID
        df_map (pd.DataFrame): Mapping dataframe
        wf_name (str): Name of the Wind Farm

    Returns:
        pd.DataFrame: Output dataframe
    """
    
    # Pivot
    df_melted = pd.melt(
        df, id_vars=["datetime"], var_name="variable", value_name="value")
    
    # Separate 'type' (i.e. statistic) and 'variable'
    df_melted['type'] = df_melted['variable'].str.extract(r'(MinValue|MaxValue|AvgValue|Samples)$')
    df_melted['variable'] = df_melted['variable'].str.replace(r'_(MinValue|MaxValue|AvgValue|Samples)$', '', regex=True)
   
    # Pivot again the variables as columns
    df = df_melted.pivot(index=['datetime','type'], columns=['variable'], values='value').reset_index()

    # Keep only mapping variables
    lst_orig_variables = df_map['origin_variable'].to_list()
    lst_columns = ['datetime', 'type'] + lst_orig_variables
    df = df[lst_columns]
 
    # Renaming dictionary
    lst_old_cols = [row["origin_variable"] for _, row in df_map.iterrows()]
    dict_old_to_new = {
        row["origin_variable"]: row["variable_internal"] for _, row in df_map.iterrows()
    }
    dict_old_to_new['datetime'] = 'timestamp'

    # Completing missing original signals
    for col in lst_old_cols:
        if col not in df.columns:
            logging.error(f"Missing expected signal: {col}")
            df[col] = None

    # Renaming columns
    df = df[['type'] + list(dict_old_to_new.keys())]
    df = df.rename(columns=dict_old_to_new)

    # Transform timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Identifiers
    df['met_mast_id'] = id_mm
    df['wf_name'] = wf_name
        
    # Check ranges
    df_aux = df[df['type']== 'Samples']
    df = df[df['type'] != 'Samples']
    dict_limits = {
        'air_density': {'min': 0, 'max': 3},
        'pressure': {'min': 600, 'max': 1200},
        'relative_humidity': {'min': 0, 'max': 120},
        'rain': {'min': -5000, 'max': 7000},
        'battery': {'min': 0, 'max': 20},
        'temperature': {'min': -60, 'max': 100},
        'wind_direction': {'min': 0, 'max': 365},
        'wind_speed': {'min': 0, 'max': 60}
    }
    for var,lim in dict_limits.items():

        min_value = lim['min']
        max_value =lim['max']
        df[var] = df[var].apply(lambda x: (x if(x >= min_value) & (x <= max_value) else np.nan) if x is not None else np.nan)   
    df =  pd.concat([df,df_aux],ignore_index=True)
    df = df.sort_values(by=['timestamp','type']).reset_index()
    df = df.drop(columns=['index'])

    return df
