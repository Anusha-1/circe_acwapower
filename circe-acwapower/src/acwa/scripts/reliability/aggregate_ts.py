"""
acwa.scripts.reliability.aggregate_ts

Script to aggregate reliability time-series into hour and day
"""

import logging

import acwa.db as db

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.data import obtain_aggregated_time_period

def main():

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("-------- START SCRIPT: reliability.aggregate_ts ------------")

    logging.info("Read data")
    df_ts = db.read_table_as_df(
        "reliability_ts", config['db'], "intermediate",
        chunksize=10000
    )
    df_temperature_signals = db.read_table_as_df(
        "temperature_signals", config['db'], "vis")
    lst_temp_signals = list(df_temperature_signals['name_in_origin'])
    lst_temp_signals.sort()

    for time_period in ['day', 'hour']:

        df_aux = df_ts.copy()

        logging.info(f"Time aggregated period: {time_period}")
        df_aux['time_agg'] = df_aux['timestamp'].apply(
            obtain_aggregated_time_period, args=(time_period,))
        
        logging.info("Group by data")
        lst_cols = ['id_wtg_complete', 'time_agg'] + lst_temp_signals
        df_group_data = df_aux[lst_cols].groupby(['id_wtg_complete', 'time_agg']).agg(["min", "mean", "max"])
        df_group_data.columns = ['_data_'.join(col).strip() for col in df_group_data.columns.values]

        logging.info("Group by normalized temperature")
        lst_norm_signals = [f"{signal}_normalized" for signal in lst_temp_signals]
        lst_cols = ['id_wtg_complete', 'time_agg'] + lst_norm_signals
        df_group_norm = df_aux[lst_cols].groupby(['id_wtg_complete', 'time_agg']).agg(["min", "max", "mean"])
        df_group_norm.columns = ['_'.join(col).strip() for col in df_group_norm.columns.values]

        logging.info("Group by pred")
        lst_temp_predicted_signals = []
        for signal in lst_temp_signals:
            lst_temp_predicted_signals += [f"{signal}_max", f"{signal}_min", f"{signal}_median"] 
        lst_cols = ['id_wtg_complete', 'time_agg'] + lst_temp_predicted_signals
        df_group_pred = df_aux[lst_cols].groupby(['id_wtg_complete', 'time_agg']).agg(["mean"])
        df_group_pred.columns = ['_pred_'.join(col).strip() for col in df_group_pred.columns.values]

        logging.info("Merge")
        df_group_total = df_group_data.reset_index().merge(
            df_group_pred.reset_index(), 
            on=['id_wtg_complete', 'time_agg'])
        df_group_total = df_group_total.merge(
            df_group_norm.reset_index(),
            on=['id_wtg_complete', 'time_agg']
        )
        
        logging.info("Write")
        db.write_df_as_table(
            df_group_total, config['db'], "intermediate", 
            f"reliability_ts_{time_period}", index=False, chunksize=10000, 
            if_exists='replace')    


if __name__ == "__main__":
    main()