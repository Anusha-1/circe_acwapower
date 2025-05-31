"""
acwa.alarms.aggregate.code

Module to aggregate alarms (durationa and losses) by alarm code
"""

import logging
import pandas as pd

from acwa.data import extend_by_days
import acwa.losses as loss

def aggregate_alarms_per_day(
        df_oper_10min: pd.DataFrame, 
        df_alarms: pd.DataFrame,
        non_registered_alarms: bool = True) -> pd.DataFrame:
    """
    Aggregate alarms (duration and losses) by alarm code daily

    Args:
        df_oper_10min (pd.Dataframe): Oper 10min data
        df_alarms (pd.DataFrame): Alarms dataframe
        non_registered_alarms (bool, optional): Defaults to True

    Returns:
        pd.DataFrame: Dataframe with alarms of the same code sum daily
    """

    logging.info("Extend by days")
    cols_to_keep = [
        'id_wf',
        'id_wtg',
        'id_wtg_complete',
        'code',
        'component',
        'start_datetime',
        'end_datetime',
        'duration'
    ]
    df_alarms_aux = extend_by_days(df_alarms[cols_to_keep])
    df_alarms_aux['day'] = df_alarms_aux["start_datetime"].apply(lambda x: x.date())
    
    ## Add loss over extended dataframe
    logging.info("Distribute losses in alarms")
    df_alarms_aux = loss.distribute_losses_in_alarms(
        df_alarms_aux, df_oper_10min, 
        non_registered_alarms=non_registered_alarms,
        codes_to_ignore=[-2]) ## Ignore -2 (under-performing) as it is not unavailable

    ## Group by
    logging.info("Group by")
    df_group = df_alarms_aux.groupby(
        ['id_wf','id_wtg','id_wtg_complete','day', 'code', 'component']).agg(
            {'duration': 'sum',
             'losses': 'sum'}
        ).reset_index()

    return df_group
