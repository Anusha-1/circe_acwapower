
"""
acwa.alarms.join.10min.all

Module to join all data with alarms
"""

import pandas as pd

from acwa.alarms.join.min_10.windfarm import join_alarms_and_10min_data_in_windfarm

def join_alarms_and_10min_data(
        df_10min: pd.DataFrame,
        df_alarms: pd.DataFrame,
        df_wtg_config: pd.DataFrame,
        config: dict
) -> pd.DataFrame:
    """
    Join 10min and alarms on all wind farms

    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data
        df_alarms (pd.DataFrame): Dataframe with alarms
        df_wtg_config (pd.DataFrame): Dataframe with WTG configuration
        config (dict): Configuration

    Returns:
        pd.DataFrame: Data with alarms
    """
    
    lst_dfs_farms = []
    for id_wf in set(df_10min['id_wf']):

        df_10min_aux = df_10min[df_10min['id_wf']==id_wf]
        df_10min_aux = df_10min_aux.drop_duplicates() #We should fix this at source, we are generating the data wrongly

        df_aux_alarms = df_alarms[df_alarms['id_wf']==id_wf]

        df_aux_wtg_config = df_wtg_config[df_wtg_config['id_wf']==id_wf]

        df_10min_aux = join_alarms_and_10min_data_in_windfarm(
            df_10min_aux, df_aux_alarms, df_aux_wtg_config, id_wf, config
        )

        lst_dfs_farms.append(df_10min_aux)
    
    df_10min = pd.concat(lst_dfs_farms)

    return df_10min
