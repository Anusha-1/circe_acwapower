"""
acwa.data.compilation.mapping.min_10.khalladi_pitch

Module to map signals from pitch table in Khalladi
"""

import pandas as pd

from ..general import map_from_table_with_turbine_columns

def map_10min_pitch_Khalladi(
        df: pd.DataFrame,
        id_wf: str,
        df_map: pd.DataFrame
) -> pd.DataFrame:
    """    
    Function to map 10-min data pitch signals with Khalladi format to standard 
    format
    
    Args:
        df (pd.DataFrame): DataFrame with raw data
        id_wf (int): Wind Farm ID
        df_map (pd.DataFrame): DataFrame with variable mapping

    Returns:
        pd.DataFrame: DataFrame with standard format
    """
    

    # Special formatting for pitch angles in Khalladi (Tripiclate data for blades)
    df = df.copy()
    duplicated_cols = {f"{col} {suffix}": df[col] for col in df.columns if col != "PCTimeStamp" for suffix in ["A", "B", "C"]}
    df_duplicated = pd.DataFrame(duplicated_cols)
    df = pd.concat([df, df_duplicated], axis=1)
    # NOTE: See if its possible to have this data in origin

    df = map_from_table_with_turbine_columns(
        df, df_map, "PCTimeStamp"
    )

    # Add and format identifiers
    df['id_wf'] = id_wf
    df['id_wtg'] = "V" + df['id_wtg']
    df['id_wtg_complete'] = df.apply(
        lambda row: f"{row['id_wf']}-{row['id_wtg']}",
        axis=1
    )

    return df
