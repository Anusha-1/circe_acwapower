"""
acwa.scripts.metadata.densities

Script to upload table with densities info
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging
from acwa.tables import DensitiesSchema

def main():


    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------ START SCRIPT: metadata.densities --------------")

    logging.info("Reading file")
    input_path = pathlib.Path(
        "input",
        "metadata", 
        "densities.csv")
    config = read_config()
    df = pd.read_csv(
        read_file(input_path, config['file_storage'], container='data')
    )

    logging.info("Validate Schema")
    DensitiesSchema.validate(df)

    logging.info("Writing table")
    write_df_as_table(
        df, 
        config['db'], 
        "vis", 
        "densities", 
        if_exists="replace",
        chunksize=10000,
        index=False)     

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
