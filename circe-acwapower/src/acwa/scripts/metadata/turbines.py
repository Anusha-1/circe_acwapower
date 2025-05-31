"""
acwa.scripts.metadata.turbines

Script to load metadata table with WTG definition
"""

from datetime import datetime
import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_file
from acwa.log import format_basic_logging
from acwa.tables import WtgConfigSchema

def main():


    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------- START SCRIPT: metadata.turbines --------------")

    logging.info("Reading file")
    input_path = pathlib.Path(
        "input",
        "metadata", 
        "wtg_config.csv")
    config = read_config()
    df = pd.read_csv(
        read_file(input_path, config['file_storage'], container='data')
    )

    logging.info("Format")
    df['contractual_date'] = df['contractual_date'].apply(
        lambda x: datetime.strptime(x, "%d/%m/%Y").date()
    )
    
    logging.info("Validate Schema")
    df = df[WtgConfigSchema.to_schema().columns.keys()] 
    WtgConfigSchema.validate(df)

    logging.info("Writing table")
    write_df_as_table(
        df, 
        config['db'], 
        "vis", 
        "wtg_config", 
        if_exists="replace",
        chunksize=10000,
        index=False)     

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
