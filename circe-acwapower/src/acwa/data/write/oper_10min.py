"""
acwa.data.write.oper_10min

Module to write vis.oper_10min
"""

import logging

import pandas as pd

from acwa.db import write_df_as_table, run_query_in_transaction
from acwa.tables import Oper10minSchema

def write_oper_10min(
        df_10min: pd.DataFrame, 
        incremental: bool, 
        config_db: dict):
    """
    Write table vis.oper_10min

    Args:
        df_10min (pd.DataFrame): Dataframe with 10 min data
        incremental (bool): Incremental flag
        config_db (dict): Configuration of database
    """
    
    output_table_name = 'oper_10min'
    output_schema = 'vis'

    ## Correction needed if the pitch data is not updated.
    ## All the angles are None and taken as object by default, we need to transform to float
    df_10min['pitch_angle_average'] = df_10min['pitch_angle_average'].astype(float)
    df_10min['manufacturer_performance_loss'] = df_10min['manufacturer_performance_loss'] .astype(float)

    df_10min = df_10min[Oper10minSchema.to_schema().columns.keys()] 
    Oper10minSchema.validate(df_10min)
    
    if incremental:
        result = run_query_in_transaction(
            "delete_last_10min",
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
