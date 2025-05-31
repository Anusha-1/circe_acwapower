"""
acwa.scripts.reliability.aggregate_heatmaps

Script to aggregate reliability results for the building of heatmaps
"""

import logging

import acwa.db as db

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.data import obtain_aggregated_time_period

def main():

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("----- START SCRIPT: reliability.aggregate_heatmaps ---------")

    logging.info("Read data")
    df_ts = db.read_table_as_df(
        "reliability_ts", config['db'], "intermediate",
        chunksize=10000
    )
    df_temperature_signals = db.read_table_as_df(
        "temperature_signals", config['db'], "vis")
    lst_temp_signals = list(df_temperature_signals['name_in_origin'])
    lst_temp_signals.sort()

    logging.info("Time aggregated period: day")
    df_ts['day'] = df_ts['timestamp'].apply(
            obtain_aggregated_time_period, args=('day',))
    
    logging.info("Group by normalized temperature")
    lst_cols = ['id_wtg_complete', 'day'] + [f"{x}_normalized" for x in lst_temp_signals]
    df_group_norm = df_ts[lst_cols]\
        .groupby(['id_wtg_complete','day'], dropna=True)\
        .agg(['sum','count','mean'])
    df_group_norm.columns = ['_'.join(col).strip() for col in df_group_norm.columns.values]
    
    logging.info("Group by over-temperature time")
    lst_cols = ['id_wtg_complete', 'day'] + [f"{x}_over" for x in lst_temp_signals]
    df_group_time = df_ts[lst_cols]\
        .groupby(['id_wtg_complete','day'], dropna=True)\
        .agg(['sum','count','mean'])
    df_group_time.columns = ['_'.join(col).strip() for col in df_group_time.columns.values]
    
    logging.info("Merge")
    df_group_total = df_group_norm.reset_index().merge(
        df_group_time.reset_index(), 
        on=['id_wtg_complete', 'day'])
    
    logging.info("Write")
    db.write_df_as_table(
        df_group_total, config['db'], "intermediate", 
        "reliability_heatmaps", index=False, chunksize=10000, 
        if_exists='replace')    

if __name__ == "__main__":
    main()
    