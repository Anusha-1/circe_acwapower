"""
acwa.scripts.static_load.met_mast

Script to create raw static table with met mast data
"""

import logging
import pathlib
import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_excel
from acwa.log import format_basic_logging

def main():

    # NOTE: Make sure you have these files inside your file_storage.root_path
    # (Check your configuration at config/main.yml)

    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])
    
    logging.info("------------ START SCRIPT: static_load.met_mast ------------")

    
    logging.info("Loading met mast metadata")
    met_mast_lst = ['Kh-M1','Az-M1']
    mast_dict = {
        'Kh-M1': ['MET MAST DATA OF 2023.xlsx','MET MAST DATA OF 2024.xlsx'], 
        'Az-M1': ['MET MAST DATA OF 2023.xlsx','MET MAST DATA OF 2024.xlsx']
        }
    
    for mast in met_mast_lst:
        df_lst = []
        logging.info(f"Loading {mast} met mast data")
        for file in mast_dict[mast]:
            input_path = pathlib.Path(
                "input", 
                "Historical data", 
                file)
            df = read_excel(input_path, config['file_storage'], container='data')
            df_lst.append(df)
        df = pd.concat(df_lst)
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'], yearfirst = True )
        df = df[df['PCTimeStamp']>'2023-01-12']
        logging.info("Writting mast met mast data")
        write_df_as_table(
                df, 
                config['db'], 
                "raw", 
                f'static_met_mast_{mast}', 
                if_exists='replace',
                index=False,
                chunksize=10000)

if __name__ == "__main__":
    main()
