"""
acwa.data.write.alarms_with_losses

Module to write intermediate.alarms_with_losses
""" 

import logging

import pandas as pd

from acwa.db import write_df_as_table, run_query
from acwa.tables import AlarmsLossesSchema

def write_alarms_with_losses(
        df_alarms: pd.DataFrame, 
        incremental: bool, 
        config_db: dict):
    """
    Write the table intermediate.alarms_with_losses

    Args:
        df_alarms (pd.DataFrame): Dataframe of alarms
        incremental (bool): Incremental flag
        config_db (dict): Configuration of database
    """

    output_table_name = 'alarms_with_losses'
    output_schema = 'intermediate'

    df_alarms = df_alarms.reset_index().rename(columns={'index': 'id_event'})
   
    ## Temporary format time between alarms
    df_alarms['priority'] = df_alarms['priority'].astype("Int64")

    ## Format types (needed for len(df_alarms) == 0)
    df_alarms['code'] = df_alarms['code'].astype('Int64')
    df_alarms['duration'] = df_alarms['duration'].astype('Int64')
    df_alarms['ongoing'] = df_alarms['ongoing'].astype('bool8')
    df_alarms['serial_number'] = df_alarms['serial_number'].astype('Int64')
    df_alarms['severity'] = df_alarms['severity'].astype('Int64')
    df_alarms['severity_scale'] = df_alarms['severity_scale'].astype('Int64')  

    AlarmsLossesSchema.validate(df_alarms)
    df_alarms = df_alarms[AlarmsLossesSchema.to_schema().columns.keys()]

    if incremental:

        result = run_query(
            "delete_last_alarms",
            config_db,
            returns="Cursor"
        )
        logging.info(f"Rows deleted: {result.rowcount}")

        write_df_as_table(
            df_alarms,
            config_db,
            output_schema,
            output_table_name,
            if_exists='append',
            index=False
        )
        logging.info(f"Rows appended: {len(df_alarms)}")
     
    else:
        write_df_as_table(
            df_alarms,
            config_db,
            output_schema,
            output_table_name,
            if_exists='replace',
            index=False
        )
