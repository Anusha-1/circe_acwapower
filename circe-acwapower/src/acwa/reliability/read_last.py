"""
acwa.reliability.read_last

Module to read the last temperature data
"""

import pandas as pd

import acwa.db as db

def read_last_temperatures(
        df_temp_signals: pd.DataFrame,
        config_db: dict) -> pd.DataFrame:
    """
    Read the temperatures for the last timestamp

    Args:
        df_temp_signals (pd.DataFrame): Dataframe with the defined temperature
            signals
        config_db (dict): Configuration of the database

    Returns:
        pd.DataFrame: Dataframe with columns id_wtg_complete, signal, 
            temperature and main_component
    """

    df_last_temperatures = db.read_table_as_df(
        "reliability_ts_last", config_db, "intermediate"
    )
    lst_temp_signals = list(df_temp_signals['name_in_origin'])
    
    ## Add temperature
    df_last_temp_aux = df_last_temperatures[['id_wtg_complete'] + lst_temp_signals]
    df_temp_melted = pd.melt(
        df_last_temp_aux, 
        id_vars=['id_wtg_complete'],
        var_name='signal',
        value_name='temperature').merge(
            df_temp_signals[['name_in_origin','main_component']].rename(
                columns={'name_in_origin': 'signal'}),
            on=['signal'], how='left')
    
    ## Add over-temperature
    lst_temp_signals_over = [f"{signal}_over" for signal in lst_temp_signals]
    df_last_temp_aux = df_last_temperatures[['id_wtg_complete'] + lst_temp_signals_over]
    df_last_temp_aux.columns = ['id_wtg_complete'] + lst_temp_signals
    df_temp_melted_aux = pd.melt(
        df_last_temp_aux, 
        id_vars=['id_wtg_complete'],
        var_name='signal',
        value_name='overtemperature')
    
    ## Merge
    df_temp_melted = df_temp_melted.merge(
        df_temp_melted_aux, 
        on=['id_wtg_complete', 'signal'],
        how='left'
    )
    
    return df_temp_melted
