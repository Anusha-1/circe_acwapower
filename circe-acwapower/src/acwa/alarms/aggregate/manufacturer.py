"""
acwa.alarms.aggregate.manufacturer

Module to aggregate alarms (durationa and losses) by manufacturer concept
"""


import pandas as pd

from acwa.data import extend_by_days
import acwa.losses as loss


def aggregate_manufacturer_per_day(
        df_oper_10min: pd.DataFrame, 
        df_alarms: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate alarms (durationa and losses) by manufacturer concept daily

    NOTE: We have copy and change the logic developed to allocate component 
    loss and time, we could generalize

    Args:
        df_oper_10min (pd.Dataframe): Oper 10min data
        df_alarms (pd.DataFrame): Alarms dataframe

    Returns:
        pd.DataFrame: Dataframe with alarms of the same code sum daily
    """

    cols_to_keep = [
        'id_wf',
        'id_wtg',
        'id_wtg_complete',
        'code',
        'manufacturer_availability',
        'start_datetime',
        'end_datetime',
        'duration'
    ]
    df_alarms_aux = extend_by_days(df_alarms[cols_to_keep])
    df_alarms_aux['day'] = df_alarms_aux["start_datetime"].apply(lambda x: x.date())

    ## Add loss over extended dataframe
    df_alarms_aux = loss.distribute_losses_in_alarms(
        df_alarms_aux, df_oper_10min, non_registered_alarms=False,
        codes_to_ignore=[-2]) ## Ignore -2 (under-performing) as it is not unavailable

    ## Group by
    df_group = df_alarms_aux.groupby(
        ['id_wf','id_wtg','id_wtg_complete','day', 'manufacturer_availability']).agg(
            {'duration': 'sum',
             'losses': 'sum'}
        ).reset_index()

    return df_group