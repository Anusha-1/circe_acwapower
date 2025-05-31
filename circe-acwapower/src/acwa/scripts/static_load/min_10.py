"""
acwa.scripts.static_load.min_10

Complete process to write the static raw input of 10 min data
"""

import logging
import pathlib

import pandas as pd

from acwa.mockup import write_static_raw_table
from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging

def main():

    # NOTE: Make sure you have these files inside your file_storage.root_path
    # (Check your configuration at config/main.yml)

    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------ START SCRIPT: static_load.min_10 --------------")

    logging.info("Loading Khalladi historical data")
    # Read file and write SQL table
    input_path = pathlib.Path(
        "input", 
        "Historical data", 
        "WINDCR_DATAMIN_TALL2023_aggregated_data_10 min.csv")
    write_static_raw_table(
        input_path,
        "static_input_10min_Khalladi",
        read_csv_kwargs={'index_col': 'index'}
    )

    logging.info("Loading Azerbaijan historical data (based on Khalladi)")
    
    logging.info("Reading original data")
    df = pd.read_csv(
        read_file(input_path, config['file_storage'], container='data'),
        index_col='index'
    )

    logging.info("Transforming data")
    ## Filter to first 11 turbines
    df = df[df['turbine_id'] < 12]

    logging.info("Write table")
    write_df_as_table(
        df, 
        config['db'], 
        "raw", 
        "static_input_10min_Azerbaijan", 
        if_exists="replace",
        index=False,
        chunksize=10000)
    
    logging.info("---------------------- FINISH ------------------------------")

if __name__ == "__main__":
    main()