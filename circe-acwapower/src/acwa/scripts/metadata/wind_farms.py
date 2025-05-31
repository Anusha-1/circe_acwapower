"""
acwa.scripts.metadata.wind_farms

Writes table about fleet from file
"""

from datetime import datetime

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging
from acwa.tables import WfConfigSchema

def main():

    # NOTE: Make sure you have these files inside your file_storage.root_path
    # (Check your configuration at config/main.yml)
  
    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------ START SCRIPT: metadata.wind_farms -------------")


    logging.info("Read input data")
    input_path = pathlib.Path(
        "input", 
        "metadata",
        "wf_config.csv")    
    df = pd.read_csv(
        read_file(input_path, config['file_storage'], container='data')
    )

    logging.info("Format dates")
    df['reference_start'] = df['reference_start'].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d").date())
    df['reference_end'] = df['reference_end'].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d").date())

    logging.info("Validating Schema")
    WfConfigSchema.validate(df)
    df = df[WfConfigSchema.to_schema().columns.keys()]

    logging.info("Write table")
    write_df_as_table(
        df, 
        config['db'], 
        "vis", 
        "wf_config", 
        if_exists="replace",
        chunksize=10000,
        index=False)

if __name__ == "__main__":
    main()
    