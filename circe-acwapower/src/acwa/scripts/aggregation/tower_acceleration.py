"""
acwa.scripts.aggregation.tower_acceleration

Module to aggregate the tower acceleration data to build histograms
"""

import itertools
import logging
import math

import pandas as pd

import acwa.data as data

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.log import format_basic_logging
from acwa.tables import TowerAcceleration1DaySchema

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------ START SCRIPT: aggregation.tower_acceleration --------")

    min_acc = -100
    max_acc = 100
    delta = 5

    logging.info("Read collected tower acceleration data") 
    df_data = data.read_input_tower_xy_data(config['db'])

    logging.info("Format data")
    df_data = data.melt_tower_xy_data(df_data)

    logging.info("Build empty complete dataframe")
    lst_wtg = list(set(df_data['id_wtg_complete']))
    lst_wtg.sort()
    day_max = df_data['timestamp'].max().date()
    day_min = df_data['timestamp'].min().date()
    lst_dates = pd.date_range(start=day_min, end=day_max, freq='1D')
    lst_bins_left = range(min_acc, max_acc, delta)
    lst_directions = ['X','Y']
    
    lst_records = []
    for wtg, day, bin_left, dir in itertools.product(lst_wtg, lst_dates, lst_bins_left, lst_directions):
        record = {
            'id_wtg_complete': wtg,
            'day': day,
            'acceleration_binned': bin_left + 0.5*delta,
            'direction': dir 
        }
        lst_records.append(record)
    df_complete = pd.DataFrame.from_records(lst_records)
    df_complete['day'] = df_complete['day'].dt.date

    logging.info("Obtain values from real data")
    df_data = df_data[df_data['statistic']=='avg']
    df_data = df_data[df_data['value']!=0]
    df_data = df_data.dropna(subset=['value'])
    
    df_data['day'] = df_data['timestamp'].dt.date
    df_data['acceleration_binned'] = df_data['value'].apply(
        lambda x: min_acc + math.floor((x-min_acc)/delta)*delta + 0.5*delta
    )
    
    df_group = df_data\
        .groupby(['id_wtg_complete', 'day', 'acceleration_binned', 'direction'])\
        .agg(count=('timestamp','count'))\
        .reset_index()

    logging.info("Merge")
    df_final = df_complete.merge(
        df_group,
        on=['id_wtg_complete', 'day', 'acceleration_binned', 'direction'],
        how='left'
    )
    df_final['count'] = df_final['count'].fillna(0).astype('int64')

    logging.info("Writing table")
    TowerAcceleration1DaySchema.validate(df_final)
    write_df_as_table(df_final, config['db'], 'vis', 'tower_acceleration_1day',
                      chunksize=10000, index=False, if_exists='replace')

if __name__ == '__main__':
    main()

