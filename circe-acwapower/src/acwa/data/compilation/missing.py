"""
acwa.data.compilation.missing

Complete and warn about missing signals
"""

import logging

import pandas as pd

def complete_missing_signals(
        df_data: pd.DataFrame,
        df_var: pd.DataFrame
) -> pd.DataFrame:
    """
    Function to complete missing signals data

    Args:
        df_data (pd.DataFrame): Dataframe with collected signals
        df_var (pd.DataFrame): Dataframe with all the signals

    Returns:
        pd.DataFrame: Completed dataframe
    """
    
    # List of missing signals
    missing_columns = [
        col for col in df_var['variable_internal'][df_var['variable_type'].isin(['essential', 'required'])].to_list()
        if col not in df_data.columns
    ]

    # Warnings
    for col in missing_columns:
        logging.warning(f"Missing signal {col}")

    # Concat with null columns for missing signals
    df_data = pd.concat(
        [df_data, pd.DataFrame({col: None for col in missing_columns}, 
                               index=df_data.index)], 
        axis=1)

    return df_data
