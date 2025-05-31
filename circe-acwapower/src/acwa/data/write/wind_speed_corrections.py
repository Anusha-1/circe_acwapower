"""
acwa.data.write.wind_speed_corrections

Module to write intermediate.wind_speed_corrections
"""

import logging

import pandas as pd

from acwa.db import write_df_as_table, run_query_in_transaction
from acwa.tables import WindSpeedCorrectionsSchema

def write_wind_speed_corrections(
        df_10min: pd.DataFrame, 
        incremental: bool, 
        config_db: dict,
        data_type: str = '10min'):
    """
    Write table intermediate.wind_speed_corrections

    Args:
        df_10min (pd.DataFrame): Dataframe with 10 min data
        incremental (bool): Incremental flag
        config_db (dict): Configuration of database
        data_type (str, optional): "10min" or "1min". Defaults to "10min"
    """
    
    output_table_name = f"wind_speed_corrections_{data_type}"
    output_schema = 'intermediate'

    df_10min = df_10min[WindSpeedCorrectionsSchema.to_schema().columns.keys()] 
    WindSpeedCorrectionsSchema.validate(df_10min)
    
    if incremental:
        result = run_query_in_transaction(
            f"delete_last_{data_type}_corrections",
            config_db,
            returns="Cursor"
        )
        logging.info(f"Rows deleted: {result.rowcount}")

        write_df_as_table(
            df_10min,
            config_db,
            output_schema,
            output_table_name,
            if_exists='append',
            index=False
        )
        logging.info(f"Rows appended: {len(df_10min)}")
     
    else:
        write_df_as_table(
            df_10min,
            config_db,
            output_schema,
            output_table_name,
            index=False,
            if_exists="replace",
            chunksize=10000
        )
