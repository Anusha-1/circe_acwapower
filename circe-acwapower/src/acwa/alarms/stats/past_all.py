"""
acwa.alarms.stats.past_all

Module to complete alarms information from previous alarms
"""

import pandas as pd

from acwa.alarms.stats.past_turbines import add_past_times

def calculate_alarm_stats(df_alarms: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate alarms information from previous alarms (time since previous 
    alarm) 

    Args:
        df_alarms (pd.DataFrame): Dataframe with all the alarms

    Returns:
        pd.DataFrame: Dataframe with extra columns 
    """

    turbine_list = list(set(df_alarms['id_wtg_complete']))
    turbine_list.sort()
    lst_dfs = []
    for turb in turbine_list:

        df_aux = df_alarms[df_alarms['id_wtg_complete']==turb].copy().reset_index()        
        df_aux = add_past_times(df_aux)
        lst_dfs.append(df_aux)
        
    return pd.concat(lst_dfs, ignore_index=True)