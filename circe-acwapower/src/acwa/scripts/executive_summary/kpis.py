"""
acwa.scripts.executive_summary.kpis

Script to summarize KPIs for executive summary
"""

import logging

import pandas as pd

import acwa.data as data

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging
from acwa.tables import ExecutiveSummaryKPI

def main():
    
    config = read_config()
    format_basic_logging(config['log'])

    logging.info("---------- START SCRIPT: executive_summary.kpis ------------")

    df_wtg_config = read_table_as_df("wtg_config", config['db'], "vis")

    logging.info("Read data")
    df_oper_1day = read_table_as_df("oper_1day", config['db'], "vis")
    ids_to_keep = ['id_wf', 'id_wtg_complete', 'day']
    cols_to_keep = [
        'energy', 'cp', 'contractual_available_time', 'contractual_total_time', 
        'count_data_ok', 'count_data_total', 'manufacturer_performance_loss', 
        'wind_speed', 'p50', 'p75', 'p90', 'p99' 
    ]
    df_oper_1day = df_oper_1day[ids_to_keep + cols_to_keep] 

    logging.info("Obtain temporal groups")
    df_oper_1day['month'] = df_oper_1day['day'].dt.strftime("%B")
    df_oper_1day['year'] = df_oper_1day['day'].dt.strftime("%Y")

    logging.info("Weighted sums")
    df_oper_1day['weighted_cp'] = df_oper_1day['count_data_ok'] * df_oper_1day['cp']
    df_oper_1day['weighted_wind_speed'] = df_oper_1day['count_data_ok'] * df_oper_1day['wind_speed'] 
    
    logging.info("Group by complete months")
    df_group_months = data.sum_kpis_at_wind_farm(
        df_oper_1day, 
        cols_to_keep + ['weighted_cp', 'weighted_wind_speed'],
        ['year', 'month'])
    
    logging.info("Group by year")
    df_group_year = data.sum_kpis_at_wind_farm(
        df_oper_1day,
        cols_to_keep + ['weighted_cp', 'weighted_wind_speed'],
        ['year']
    )
    df_group_year['month'] = 'All'

    logging.info("Group by general months")
    df_group_general_months = data.sum_kpis_at_wind_farm(
        df_oper_1day,
        cols_to_keep + ['weighted_cp', 'weighted_wind_speed'],
        ['month']
    )
    df_group_general_months['year'] = 'All'

    logging.info("Group by whole period")
    df_group_all = data.sum_kpis_at_wind_farm(
        df_oper_1day,
        cols_to_keep + ['weighted_cp', 'weighted_wind_speed']
    )
    df_group_all['month'] = 'All'
    df_group_all['year'] = 'All'

    logging.info("Concatenate")
    df_group = pd.concat(
        [df_group_months, 
         df_group_year,
         df_group_general_months,
         df_group_all]).reset_index(drop=True)
    
    logging.info("Weighted averages")
    df_group['cp'] = df_group['weighted_cp'] / df_group['count_data_total']
    df_group['wind_speed'] = df_group['weighted_wind_speed'] / df_group['count_data_total']
    df_group['contractual_availability'] = (
        df_group['contractual_available_time'] / df_group['contractual_total_time'] * 100
    )
    df_group = df_group.drop(
        columns=['weighted_cp', 'weighted_wind_speed'])
    
    logging.info("Add performance ratio")
    df_group = data.add_performance_ratio_to_kpis(
        config['db'], df_wtg_config, df_oper_1day, df_group
    )

    logging.info("Add over-temperature ratio")
    df_group = data.add_overtemperature_to_kpis(
        config['db'], df_wtg_config, df_group
    )

    logging.info("Adding ids for analysis periods")
    df_group['id_wf_period'] = df_group['id_wf'] + '-' + df_group['year'] + '-' + df_group['month'] 

    logging.info("Writing")
    ExecutiveSummaryKPI.validate(df_group)
    write_df_as_table(
        df_group, config['db'], "vis", "executive_summary_kpi",
        index=False, if_exists="replace"
    )

    logging.info("Isolating metadata table")
    df_meta = df_group[['id_wf_period', 'id_wf', 'year', 'month']].drop_duplicates()
    # Missing pandera schema
    write_df_as_table(
        df_meta, config['db'], "vis", "executive_summary_metadata",
        index=False, if_exists = 'replace'
    )

if __name__ == "__main__":
    main()
