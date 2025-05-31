"""
acwa.data.aggregate.daily

Module to aggregate daily
"""

import pandas as pd

from ..read import read_input_1min_data

def aggregate_values_from_1min(
        df_10min: pd.DataFrame,
        var:str,
        config_db: dict,
        statistic:str = 'mean',
        incremental: bool =False) -> pd.DataFrame:
    """
    Take 1-min values, aggregate into 10-min and add to existing 10 min data

    Args:
        df_10min (pd.DataFrame): Pre-existing 10-min dataframe
        var (str): Variable to aggregate and add
        config_db (dict): Database configuration
        statistic (str, optional): Statistic to aggregate. Defaults to 'mean'.
        incremental (bool, optional): If True, work in incremental mode. 
            Defaults to False.

    Returns:
        pd.DataFrame: 10-min data with added column
    """
    
    df_1min = read_input_1min_data(
        incremental, config_db=config_db, days_period = None)
    
    df_1min: pd.DataFrame = df_1min[['id_wf','id_wtg','id_wtg_complete','timestamp',var]].copy()

    df_1min["10min"] = df_1min["timestamp"].dt.ceil('10min')

    # Aggregate
    dict_agg = {
        var:statistic 
    }
    df_agg = pd.DataFrame()
    df_agg = (
        df_1min.groupby(["id_wtg_complete", "10min"])
        .agg(dict_agg)
        .reset_index()       
    )
    df_agg=df_agg.rename(columns={'10min':'timestamp'}) 
    
    if var in df_10min.columns:
        df_10min = df_10min.drop(columns=[var])
    df_10min= df_10min.merge(
        df_agg[['id_wtg_complete','timestamp',var]],
        how='left',
        on=['id_wtg_complete','timestamp'])

    return df_10min
