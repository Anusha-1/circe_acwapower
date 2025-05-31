"""
acwa.scripts.dynamic_load.min_10

Complete process to write the dynamic raw input of 10 min data
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

    logging.info("------------- START SCRIPT: dynamic_load.min_10 ------------")

    logging.info("Load WF Configuration")
    df_wf_config = read_table_as_df("wf_config", config['db'], 'vis')
    
    for i, row in df_wf_config.iterrows():
        wf_name = row['wf_name']

        logging.info(f"Write realtime for {wf_name}")

        write_dynamic_raw_table(
            f"input_10min_{wf_name}", # Input data (collection of input queries to use)
            f"realtime_input_10min_{wf_name}", # Output table to write
            config = config,
            timezone = row['tz_data'],
            now = now
        )

    logging.info("---------------------- FINISH ------------------------------")

if __name__ == "__main__":
    main()
