"""
acwa.scripts.operational.min_1

Script to update oper_1min table
"""

import logging
import pandas as pd

import acwa.alarms as alarms
import acwa.data as data
import acwa.db as db
import acwa.oper as oper
import acwa.yaw as yaw

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main(incremental: bool = True, year_offset: bool = False):
    """
    Updates oper_1min

    Args:
        incremental (bool, optional): If True, perform the algorithm only on new
            data (if possible). Defaults to True
        year_offset (bool, optional):  If True, put the present moment in 2023
            when retrieving data (True to work with mockup data in 2023, in 
            production should work with False). Defaults to False
    """

    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------- START SCRIPT: operational_1min ---------------")

    # Check incremental flag. We decide here if we will load the data 
    # incrementally, or completely    
    incremental = data.check_incremental_flag_1min(incremental, config['db'])
    logging.info(f"Loading {'incremental' if incremental else 'complete'} data")
  
    logging.info("Read 1-min input data")
    df_1min = data.read_input_1min_data(
        incremental, config['db'], year_offset = year_offset)

    logging.info("Read wtg config")
    df_wtg_config = read_table_as_df('wtg_config', config['db'], 'vis')

    alarms_metadata = read_table_as_df('alarms_metadata',config['db'],'vis')

    logging.info("Read alarms and join it with data")
    df_alarms = db.read_table_as_df("input_alarms", config['db'], "intermediate")
    df_alarms = pd.merge(df_alarms,alarms_metadata, how = 'left',on= 'code')
    df_alarms = alarms.avoid_overlapping_alarms(df_alarms)
    df_1min = alarms.join_alarms_and_1min_data(df_1min, df_alarms)

    logging.info("Detect missing data")
    df_1min = data.fill_gaps(df_1min, "1min")

    logging.info("Yaw static calculations")
    df_1min = yaw.calculate_yaw_static_variables(df_1min)

    logging.info("Calculate air density")
    df_met_mast = read_table_as_df('oper_met_mast',config['db'],'vis')
    met_mast_config = read_table_as_df('met_mast_metadata',config['db'],'vis')
    df_1min = data.calculate_density_10min(
        df_1min, 
        df_wtg_config, 
        df_met_mast, 
        met_mast_config, 
        incremental=incremental,
        update_pressure=False)

    logging.info("Calculate cp")
    df_1min = oper.calculate_cp_10min(df_1min, df_wtg_config)

    logging.info("Calculate wind speed correction")
    df_1min = data.correct_speed_with_density(df_1min)

    logging.info("Calculate sector")
    df_sectors = read_table_as_df(
        "sectors",
        config['db'],
        "vis"
    )    
    df_1min = data.assign_sector_10min(
        df_1min,
        df_sectors
    )
    
    logging.info("Write oper 1 min data")
    data.write_oper_1min(df_1min, incremental, config['db'])  

    logging.info("Correct to all densities")
    df_1min_corrected = data.correct_by_densities(df_1min, config['db']) 

    logging.info("Write wind speed corrections")
    data.write_wind_speed_corrections(
        df_1min_corrected, incremental, config['db'], 
        data_type='1min')
    
    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main(incremental=True)
    