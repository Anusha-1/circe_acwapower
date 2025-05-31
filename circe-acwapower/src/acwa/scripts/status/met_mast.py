"""
acwa.scripts.status

Script to obtain status table
"""

import logging

import pandas as pd
import numpy as np

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.db import run_query, write_df_as_table, read_table_as_df
from acwa.tables import MetMastSchema


def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("-------------- START SCRIPT: status.met_mast ---------------")

    output_table_name = 'status_met_mast'
    logging.info('loading wtg list')
    df_wtg_config = read_table_as_df('wtg_config',config['db'], 'vis')
    df_wtg_config = df_wtg_config[['id_wtg_complete','met_mast_id']]


    logging.info("Obtain last 10-min")
    df_met_mast: pd.DataFrame = run_query(
        "select_last_10min_per_met_mast",
        config['db'],
        returns="Dataframe"
    )
    df_met_mast = df_met_mast.map(lambda x: np.nan if x is None else x)
    df_met_mast = df_met_mast[MetMastSchema.to_schema().columns.keys()]
    df_met_mast['timestamp'] = pd.to_datetime(df_met_mast['timestamp'], errors='coerce')
    df_met_mast = pd.merge(df_wtg_config,df_met_mast,'left','met_mast_id' )

    
    logging.info("Writing table")
    MetMastSchema.validate(df_met_mast[df_met_mast['type'] != 'Samples'])
    write_df_as_table(
        df_met_mast,
        config['db'],
        'vis',
        output_table_name,
        index=False,
        if_exists="replace"
    )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()