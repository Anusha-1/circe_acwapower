"""
acwa.data.compilation.mapping.general.turbine_columns

Module with general functions to map variables from tables structured by
turbine columns

| timestamp | signal_1_WTG_1 | signal_1_WTG_2 | ... | signal_2_WTG_1 | ...
"""

import pandas as pd

def map_from_table_with_turbine_columns(
    df: pd.DataFrame, df_map: pd.DataFrame, timestamp_col: str,
    wtg_regex_pattern: str = r"WTG(\d+)") -> pd.DataFrame:
    """
    General function to map signals from a table where the different turbines
    signals appear in different turbines, i.e.:

    | timestamp | signal_1_WTG_1 | signal_1_WTG_2 | ... | signal_2_WTG_1 | ...

    to

    | timestamp | id_wtg | signal_1 | signal_2 | ...

    Args:
        df (pd.DataFrame): _description_
        df_map (pd.DataFrame): _description_
        timestamp_col (str): _description_
        wtg_regex_pattern (str, optional): _description_. Defaults to r"WTG(\d+)".

    Returns:
        pd.DataFrame: _description_
    """

    # Melt
    df = pd.melt(
        df, id_vars=[timestamp_col], var_name="variable", value_name="value")
    df = df.rename(columns={timestamp_col: "timestamp"})
    
    # Extract WTG
    df["id_wtg"] = df["variable"].str.extract(wtg_regex_pattern)

    # Map signals
    df["signal"] = df["variable"].replace(
        df_map["origin_variable"].to_list(), 
        df_map["variable_internal"].to_list(), 
        regex=True)
    df = df.drop(columns=['variable'])

    # Pivot signals
    df = pd.pivot_table(
        df, values='value', index=['timestamp', 'id_wtg'],
        columns=['signal'])
    
    return df.reset_index()  
