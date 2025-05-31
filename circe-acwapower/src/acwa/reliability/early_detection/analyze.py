"""
acwa.reliability.early_detection.analyze

Analyze reliability data
"""

import pandas as pd

import acwa.config as conf
import acwa.db as db

def analyze_recent_reliability_data(
        config_db: dict, df_rel: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze recent reliability data to identify "unreliable" turbines

    Args:
        config_db (dict): Database configuration
        df_rel (pd.DataFrame): Reliability recent data

    Returns:
        pd.DataFrame: Dataframe with columns:

            - id_wtg_complete
            - reliable (bool)
    """
    
    ## Melt signals
    df_signals = db.read_table_as_df("temperature_signals", config_db, "vis")
    lst_signals = [f"{x}_over" for x in list(df_signals['name_in_origin'])]
    df_rel = df_rel[['id_wtg_complete','timestamp'] + lst_signals]
    df_rel = pd.melt(
        df_rel, 
        id_vars=['id_wtg_complete','timestamp'], 
        var_name="signal", 
        value_name="overtemperature")
    df_rel['signal'] = df_rel['signal'].apply(lambda x: x[:-5])
    
    ## Group by and average overtemperature
    df_group = df_rel.groupby(['id_wtg_complete', 'signal']).agg(
        mean_overtemp = ('overtemperature','mean')
    ).reset_index()

    ## Check overtemperature > threshold
    df_group['check'] = df_group['mean_overtemp'] > conf.SIGNAL_THRESHOLD
    
    ## Count number of affected signals
    df_group_wtg = df_group.groupby(['id_wtg_complete']).agg(
        affected_signals = ("check", "sum")
    ).reset_index()

    ## Check affected turbines
    df_group_wtg['reliable'] = df_group_wtg['affected_signals'] < conf.WTG_THRESHOLD

    return df_group_wtg[['id_wtg_complete', 'reliable']]
