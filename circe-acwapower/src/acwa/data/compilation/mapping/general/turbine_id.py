"""
acwa.data.compilation.mapping.general

Module with general functions to map variables from tables with a turbine_id
column, i.e. tables with the following format

| timestamp | turbine_id | signal_1 | signal_2 | ...

"""

import logging

import pandas as pd


def map_from_table_with_turbine_id(
    df: pd.DataFrame, df_map: pd.DataFrame, turbine_col: str, timestamp_col: str
) -> pd.DataFrame:
    """
    General function to map variables from a table with a turbine ID column, i.e.:

    | timestamp_col | turbine_id_col | signal_1_local_name | signal_2_local_name | ...

    to:

    | timestamp | id_wtg | signal_1 | signal_2 | ...

    Timestamp column is transformed to datetime.

    Turbine id column is not transformed, this will need to be done at each 
    specific wind farm function.

    Args:
        df (pd.DataFrame): DataFrame with raw data
        df_map (pd.DataFrame): DataFrame with variable mapping information
        turbine_col (str): Name of turbine id column
        timestamp_col (str): Name of timestamp colum

    Returns:
        pd.DataFrame: DataFrame with data in standard format
    """
    
    # Preparing the renaming dictionary
    lst_old_cols = [row["origin_variable"] for _, row in df_map.iterrows()]
    dict_old_to_new = {
        row["origin_variable"]: row["variable_internal"] for _, row in df_map.iterrows()
    }
    dict_old_to_new[turbine_col] = 'id_wtg'
    dict_old_to_new[timestamp_col] = 'timestamp'

    # Completing missing original signals
    for col in lst_old_cols:
        if col not in df.columns:
            logging.error(f"Missing expected signal: {col}")
            df[col] = None

    # Renaming columns
    df = df[dict_old_to_new.keys()]
    df = df.rename(columns=dict_old_to_new)

    # Transform timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df
