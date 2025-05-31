"""
acwa.actions.static_raw_table

Module with function to create a static raw table
"""

import logging
import pathlib
import warnings

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file

def write_static_raw_table(
        input_file_path: pathlib.Path,
        table_name: str,
        read_csv_kwargs: dict = {},
        config: dict | None = None,
        if_exists: str = "replace",
        first_chunk: int = 0
) -> None:
    """
    Take a raw input file and write is as is in a SQL database

    Args:
        input_file_path (pathlib.Path): Path to the input file 
            (relative to storage root)
        table_name (str): Name of the table
        read_csv_kwargs (dict, optional): Optional kwargs for inner pandas 
            read_csv method.
        config (dict | None, optional): Configuration options. If None, it will
            read the file. Defaults to None. 
        if_exists (str, optional): How to act when table exists. Options are:
            "replace", "append". Defaults to "replace"
        first_chunk (int, optional): First chunk to write
    """

    if config is None:
        config = read_config()

    warnings.filterwarnings("ignore")
    if 'chunksize' not in read_csv_kwargs.keys():

        ## Step 1: Read the input data
        logging.info("Reading")
        df = pd.read_csv(
            read_file(input_file_path, config['file_storage'], container='data'),
            **read_csv_kwargs
        )

        ## Step 2: Write as database table
        logging.info("Writing")
        write_df_as_table(
            df, 
            config['db'], 
            "raw", 
            table_name, 
            if_exists=if_exists,
            index=False,
            chunksize=10000)

    else:
        logging.info("Reading")
        df_generator = pd.read_csv(
            read_file(input_file_path, config['file_storage'], container='data'),
            **read_csv_kwargs)
        counter = 0

        logging.info("Writing")
        for df in df_generator:
            
            counter += 1
            
            if counter >= first_chunk:
                logging.info(f"Writing chunk {counter}")
                write_df_as_table(
                    df, 
                    config['db'], 
                    "raw", 
                    table_name, 
                    if_exists='replace' if counter == 1 else 'append',
                    index=False,
                    chunksize=10000)