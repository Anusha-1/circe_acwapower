"""
acwa.data.compilation.mapping.min_10.khalladi

Mapping function for Khalladi-like 10-min signals
"""

import pandas as pd

from ..general import map_from_table_with_turbine_id

def map_10min_Khalladi(
        df: pd.DataFrame, 
        id_wf: str,
        df_map: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to map 10-min data signals with Khalladi format to standard format
    
    Args:
        df (pd.DataFrame): DataFrame with raw data
        id_wf (int): Wind Farm ID
        df_map (pd.DataFrame): DataFrame with variable mapping

    Returns:
        pd.DataFrame: DataFrame with standard format
    """

    df = map_from_table_with_turbine_id(
        df, df_map, "turbine_id", "datetime"
    )

    # Add and format identifiers
    df['id_wf'] = id_wf
    df['id_wtg'] = df['id_wtg'].apply(lambda x: f"V0{x}" if x <10 else f"V{x}")
    df['id_wtg_complete'] = df.apply(
        lambda row: f"{row['id_wf']}-{row['id_wtg']}",
        axis=1
    )
  
    return df
