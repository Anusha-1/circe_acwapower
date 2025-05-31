"""
acwa.scripts.dynamic_load.met_mast

Complete process to write met mast data dynamically
"""

from datetime import datetime
import logging

from acwa.mockup import write_dynamic_raw_table
from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main(now: datetime | None = None):
    
    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])

    logging.info("---------- START SCRIPT: dynamic_load.met_mast -------------")
    
    logging.info("Load groups Configuration")
    df_wtg_config = read_table_as_df("wtg_config", config['db'], 'vis')
    df_wf_config = read_table_as_df("wf_config", config['db'], 'vis')
    df_wtg_config = df_wtg_config.merge(
        df_wf_config[['id_wf','tz_alarms']], how='left', on='id_wf'
    )
    lst_met_mast = list(set(df_wtg_config['met_mast_id']))

    logging.info("Initializing loop in unique met mast")
    for met_mast_id in lst_met_mast:

        logging.info(f"Write realtime for {met_mast_id}")

        timezone = df_wtg_config[df_wtg_config['met_mast_id'] == met_mast_id].iloc[0]['tz_alarms'] 

        write_dynamic_raw_table(
            f"met_mast_{met_mast_id}", # Input data (collection of input queries to use)
            f"realtime_met_mast_{met_mast_id}", # Output table to write
            config = config,
            timezone=timezone,
            timestamp_col='PCTimeStamp',
            timestamp_input_format="%Y-%m-%d %H:%M:%S.%f",
            now = now
        )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
