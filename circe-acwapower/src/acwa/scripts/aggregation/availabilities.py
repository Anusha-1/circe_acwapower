"""
acwa.scripts.aggregation.availabilities

Script to obtain daily availabilities
"""

import logging

import acwa.alarms as alarms
import acwa.data as data

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------- START SCRIPT: availabilities ---------------")

    logging.info("Read WTG config")
    df_wtg = read_table_as_df("wtg_config", config['db'], "vis")

    logging.info("Read oper_10min") 
    df_oper_10min = read_table_as_df("oper_10min", config['db'], "vis")

    logging.info("Read maintenance")
    df_maint = read_table_as_df("maintenance", config['db'], "intermediate")

    logging.info("Read treated alarms")
    df_alarms = read_table_as_df("treated_events", config['db'], "vis")
    logging.info(f"Number of events: {len(df_alarms)}")
    
    logging.info("Read alarms metadata")
    df_alarms_metadata = read_table_as_df(
        "alarms_metadata",
        config['db'],
        "vis"
    )

    logging.info("Aggregate daily")
    df_daily = data.aggregate_values_daily(df_oper_10min)
    df_daily = alarms.calculate_secs_with_wind_per_day(
        df_oper_10min, df_wtg, df_daily)    

    logging.info("Obtaining availability")
    df_availabilities = alarms.obtain_time_based_availabilities(
        df_alarms, df_wtg, df_daily, df_maint)  

    logging.info("Obtaining production-based availabilities")    
    df_prod_avail = alarms.obtain_production_based_availabilities(
        df_oper_10min, df_alarms_metadata)
    df_availabilities = df_availabilities.merge(
        df_prod_avail, on=["day","id_wtg_complete"])

    logging.info("Merging data")
    df = df_daily.merge(df_availabilities,  on=["day","id_wtg_complete"])    

    logging.info("Obtaining budget production per day")
    df = data.add_daily_budget(df)
   
    logging.info("Writing oper_1day")
    data.write_oper_1day(df, config['db'])     
    
    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
    