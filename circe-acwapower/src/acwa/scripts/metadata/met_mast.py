"""
acwa.scripts.metadata.met_mast

Script to upload table with met mast info
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging
from acwa.tables import MetMastMetadataSchema

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------ START SCRIPT: metadata.met_mast ---------------")

    logging.info("Reading file")
    input_path = pathlib.Path(
        "input",
        "metadata", 
        "met_mast_metadata.csv")
    
    df = pd.read_csv(
        read_file(input_path, config['file_storage'], container='data'),
    )

    logging.info("Validate Schema")
    MetMastMetadataSchema.validate(df)

    logging.info("Writing table")
    write_df_as_table(
        df, 
        config['db'], 
        "vis", 
        "met_mast_metadata", 
        if_exists="replace",
        chunksize=10000,
        index=False)     

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
