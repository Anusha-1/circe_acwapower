"""
acwa.scripts.static_load.min_1

Complete process to write the static raw input of 1 min data
"""

import logging
import pathlib

import pandas as pd

from acwa.mockup import write_static_raw_table
from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging

def main(
        first_chunk: int = 0, 
        lst_wf: list[str] = ['Khalladi','Azerbaijan']):
    """
    Loads 1-minute data file into data tables

    Args:
        first_chunk (int, optional): First chunk of data to upload. It allows to
            continue interrupting processes. Defaults to 0.
        lst_wf (list[str], optional): List of Wind Farms to upload. 
            Defaults to ['Khalladi','Azerbaijan'].
    """

    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------- START SCRIPT: static_load.min_1 --------------")

    if 'Khalladi' in lst_wf:
        logging.info("Loading Khalladi historical data")
        input_path = pathlib.Path(
            "input", 
            "Historical data", 
            "WINDCR_DATAMIN_TALL2023_1 min.csv")
        write_static_raw_table(
            input_path,
            "static_input_1min_Khalladi",
            read_csv_kwargs={'chunksize': 100000},
            first_chunk = first_chunk
        )

    if "Azerbaijan" in lst_wf:
        logging.info("Loading Azerbaijan historical data (based on Khalladi)")    
        logging.info("Reading original data")
        df_generator = pd.read_csv(
            read_file(input_path, config['file_storage'], container='data'),
            chunksize=500000
        )

        counter = 0
        for df in df_generator:

            counter += 1

            logging.info("Transforming data")
            ## Filter to first 11 turbines
            df = df[df['turbine_id'] < 12]

            logging.info("Write table")
            write_df_as_table(
                df, 
                config['db'], 
                "raw", 
                "static_input_1min_Azerbaijan", 
                if_exists='replace' if counter == 1 else 'append',
                index=False,
                chunksize=10000)
    
    logging.info("--------------------- FINISH -------------------------------")
  
if __name__ == "__main__":
    main()
