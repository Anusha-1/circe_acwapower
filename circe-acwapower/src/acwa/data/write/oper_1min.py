"""
acwa.data.write.oper_1min

Module to write vis.oper_1min
"""

import logging

import pandas as pd

from acwa.db import write_df_as_table, run_query_in_transaction
from acwa.tables import Oper1minSchema

def write_oper_1min(
        df_1min: pd.DataFrame, 
        incremental: bool, 
        config_db: dict):
    """
    Write table vis.oper_1min

    Args:
        df_1min (pd.DataFrame): Dataframe with 1 min data
        incremental (bool): Incremental flag
        config_db (dict): Configuration of database
    """
    
    output_table_name = 'oper_1min'
    output_schema = 'vis'

    # Format (only needed when all values are NaN)
    # This should be solved at reading...
    df_1min['timestamp'] = pd.to_datetime(df_1min['timestamp']) # TO solve specific problem in Azure, due to how the original data was loaded...
    df_1min['wind_speed'] = df_1min['wind_speed'].astype(float)
    df_1min['power'] = df_1min['power'].astype(float)
    df_1min['temperature'] = df_1min['temperature'].astype(float)
    df_1min['wind_direction'] = df_1min['wind_direction'].astype(float)
    df_1min['nacelle_direction'] = df_1min['nacelle_direction'].astype(float)
    df_1min['angle_deviation'] = df_1min['angle_deviation'].astype(float)
    

    df_1min['angle_deviation_sign'] = df_1min['angle_deviation_sign'].astype("Int64")
    df_1min['yaw_yawstatesyawcw_b'] = df_1min['yaw_yawstatesyawcw_b'].astype("float64")

    df_1min = df_1min[Oper1minSchema.to_schema().columns.keys()] 
    Oper1minSchema.validate(df_1min)
    
    if incremental:
        result = run_query_in_transaction(
            "delete_last_1min",
            config_db,
            returns="Cursor"
        )
        logging.info(f"Rows deleted: {result.rowcount}")

        write_df_as_table(
            df_1min,
            config_db,
            output_schema,
            output_table_name,
            if_exists='append',
            index=False
        )
        logging.info(f"Rows appended: {len(df_1min)}")
     
    else:
        write_df_as_table(
            df_1min,
            config_db,
            output_schema,
            output_table_name,
            index=False,
            if_exists="replace",
            chunksize=10000
        )
