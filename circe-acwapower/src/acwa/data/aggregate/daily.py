"""
acwa.data.aggregate.daily

Module to aggregate daily
"""

from datetime import timedelta

import pandas as pd

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging



def aggregate_values_daily(df: pd.DataFrame):
    """
    Aggregate values daily from 10 min data

    Args:
        df (pd.DataFrame): full oper_10min df.
    """

    # Transform to energy units
    df["energy"] = df["power"] / 6  # transform from kw*10min to kwh
    df["energy"] = df["energy"].apply(lambda x: max(x, 0))
    df["producible"] = df["producible"] / 6
    df["loss"] = df["loss"] / 6

    df["manufacturer_performance_loss"] = df["manufacturer_performance_loss"] / 6
    df["historical_performance_loss"] = df["historical_performance_loss"] / 6


    df["day"] = df["timestamp"].apply(
        lambda x: (x - timedelta(seconds=1)).date())
    ## We substract a delta because the timestamp always refers to the end of 
    ## the period. Thus, the timestamp 0:00 is the last of the previous day, not
    ## the first of the current date.
    
    # Aggregate
    dict_agg = {
        "wind_speed": "mean",
        "wind_speed_corrected": "mean",
        "loss": "sum",
        "producible": "sum",
        "energy": "sum",
        "cp": "mean",
        "manufacturer_performance_loss": "sum",
        "historical_performance_loss": "sum",
        "validation_status": "sum",
        "timestamp": "count", ## Simple counter of the number of timestamps in a day (=144, except current and first day)
    }
    df_daily = pd.DataFrame()
    df_daily = (
        df.groupby(["id_wtg_complete", "day"])
        .agg(dict_agg)
        .reset_index()
        .rename(columns={
            "validation_status": "count_data_ok",
            "timestamp": "count_data_total"
        })
    )

    # Add production ratio
    df_daily['production_ratio'] = df_daily['energy'] / df_daily['producible']
    df_daily.loc[df_daily["production_ratio"] == float('-inf'), "production_ratio"] = 1
    df_daily.loc[df_daily["production_ratio"] == float('inf'), "production_ratio"] = 1


    # Add energy availability
    df_daily['energy_availability'] = df_daily['energy'] / (df_daily['energy'] + df_daily['loss'])
    df_daily.loc[df_daily["energy_availability"] == float('-inf'), "energy_availability"] = 1
    df_daily.loc[df_daily["energy_availability"] == float('inf'), "energy_availability"] = 1
    # NOTE: This corresponds to production-based availability User view

    # Add data availability
    df_daily['data_availability'] = df_daily["count_data_ok"] / df_daily["count_data_total"] * 100

    return df_daily

def add_daily_budget(df_1day:pd.DataFrame):
    
    config = read_config()
    format_basic_logging(config['log'])
   
    df_AEP = read_table_as_df(
        "AEP_table",
        config['db'],
        "vis"
    )

    dict_month = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
    }
    df_AEP['month'] = pd.to_datetime(df_AEP['timestamp']).dt.month
    df_1day['month'] = pd.to_datetime(df_1day['day']).dt.month
    
   
    def get_days_in_month(month):
        return dict_month.get(month, "Invalid month")

    df_AEP['days_in_month'] = df_AEP['month'].map(get_days_in_month) 
    
    
    for var in ['P50','P75','P90','P99']:
        df_AEP[f"daily_{var}"] = df_AEP[var]/df_AEP['days_in_month']*1000000 #from Gwh to kwh

    df_1day = pd.merge(df_1day,df_AEP[['id_wtg_complete','month','daily_P50','daily_P75','daily_P90','daily_P99']],on= ['month','id_wtg_complete'], how='left')
           ##do it with a merge, then change timestamp in AEP table? maybe in this script or in the table

    df_1day =df_1day.rename(columns= {'daily_P50': 'p50','daily_P75':'p75','daily_P90':'p90','daily_P99':'p99'}).drop(columns=['month'])
    
    

    return df_1day
    
    


