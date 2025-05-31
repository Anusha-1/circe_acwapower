"""
acwa.alarms.custom.all

Module to extract all custom alarms
"""

import pandas as pd

from acwa.alarms.custom.turbine import extract_custom_alarms_per_turbine

def extract_all_custom_alarms(
        df_10min: pd.DataFrame,
        df_alarms: pd.DataFrame,
        custom_type: str) -> pd.DataFrame:
    """
    Extract all custom alarms of a certain type for all turbines

    Args:
        df_10min (pd.DataFrame): 10min data. It should have the codes assigned
            for the custom alarms we want to add
        df_alarms (pd.DataFrame): Alarms data (without the custom alarms we want
            to add)
        custom_type (str): Type of custom alarm to extract. Options are:
            'Non-registered', 'Underperforming', 'Missing data'

    Returns:
        pd.DataFrame: Alarms dataframe with new custom alarms
    """
    
    list_id = list(set(df_10min['id_wtg_complete']))
    list_id.sort()
    list_dfs = []

    for i in list_id:

        df_10min_aux = df_10min[df_10min['id_wtg_complete'] == i]
        df_alarms_aux = df_alarms[df_alarms['id_wtg_complete']==i].copy()

        df_new_alarms = extract_custom_alarms_per_turbine(df_10min_aux, custom_type)
        df_alarms_aux = pd.concat([df_alarms_aux, df_new_alarms])        

        list_dfs.append(df_alarms_aux)

    return pd.concat(list_dfs, ignore_index=True)
