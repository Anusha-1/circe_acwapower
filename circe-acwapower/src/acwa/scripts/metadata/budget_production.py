"""
acwa.scripts.metadata.budget_production

Script to introduce the expected budget production by turbine and month
"""

import logging
import pathlib
import pandas as pd


from acwa.config import read_config
from acwa.files import read_file
from acwa.db import write_df_as_table

from acwa.log import format_basic_logging
from acwa.tables import AEPSchema

def main():

     # NOTE: Make sure you have these files inside your file_storage.root_path
    # (Check your configuration at config/main.yml)
  
    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])

    
    logging.info("Read table") 
        
    df = pd.read_csv(
        read_file(
        pathlib.Path('input', 'metadata', 'annual_energy_production.txt'),
        config['file_storage'],
        container='data'
        ),sep ='\t')
    df['timestamp'] = pd.to_datetime(df['timestamp'],format='%Y-%m')   

    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("Validate schemas")    
    AEPSchema.validate(df)
    df = df[AEPSchema.to_schema().columns.keys()]
    # AEPSchema.validate(references)
    # references = references[AEPSchema.to_schema().columns.keys()]

    logging.info("Write tables")
    write_df_as_table(
        df, 
        config['db'], 
        "vis", 
        "AEP_table", 
        if_exists="replace",
        chunksize=10000,
        index=False)

    
if __name__ == "__main__":
    main()
