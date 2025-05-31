"""
acwa.data.compilation.update_alarms.py

Module to update alarms input data on a pre-existing table
"""

from datetime import datetime
import logging
import pytz

from sqlalchemy import CursorResult

from acwa.db import run_query, write_df_as_table, run_query_in_transaction

from .mapping import DICT_MAP_ALARMS
from ..datetime import transform_timezone

def update_input_alarms(
        config_db: dict,
        id_wf: int,
        wf_name: str,
        timezone: str
):
    """
    Update the table intermediate.input_alarms with new data on a specific wind 
    farm.

    Args:
        config_db (dict): Database configuration
        id_wf (int): Id of wind farm
        wf_name (str): Name of wind farm
        timezone (str): Timezone
    """
    
    output_table_name = "input_alarms"
    output_schema = 'intermediate'

    # Timezones
    utc = pytz.timezone('UTC')
    data_tz = pytz.timezone(timezone)

    logging.info("Extracting last datetime")
    max_datetime = run_query(
        "max_time_alerts",
        config_db,
        params={"wind_farm_id": id_wf},
        returns="Fetchall"
    )[0][0]       
    if config_db["type"] == 'SQLite':
        max_datetime = utc.localize(
            datetime.strptime(max_datetime, "%Y-%m-%d %H:%M:%S.%f")) # Time in UTC
    else:
        max_datetime = utc.localize(max_datetime) # Time in UTC
   

    logging.info(f"Extracting recent data (after {max_datetime})")
    df = run_query(
        f"read_dynamic_alarms_{wf_name}",
        config_db,
        params={"max_datetime": max_datetime.astimezone(data_tz)},
        returns='Dataframe'
    )
    logging.info(f"{len(df)} alarms to add or update")

    logging.info("Delete last alarms in destiny table (we'll overwrite them)")
    result: CursorResult = run_query_in_transaction(
        "delete_input_recent_alarms",
        config_db,
        returns="Cursor",
        params={
            "max_datetime": max_datetime.astimezone(utc),
            "wind_farm_id": id_wf
        }
    )
    logging.info(f"{result.rowcount} alarms deleted")  

    assert len(df) >= result.rowcount, "We are losing alarms"   

    logging.info("Format")
    df = DICT_MAP_ALARMS[wf_name](df, id_wf)

    logging.info("Transform timezone")
    df = transform_timezone(df, "start_datetime", data_tz, utc)
    df = transform_timezone(df, "end_datetime", data_tz, utc)
    if config_db['type']=='Azure':
        df['start_datetime'] = df['start_datetime'].dt.tz_localize(None)
        df['end_datetime'] = df['end_datetime'].dt.tz_localize(None)

    logging.info("Writting to table")
    write_df_as_table(
        df,                
        config_db,
        output_schema,
        output_table_name,
        index=False,
        chunksize=10000,
        if_exists = "append"
    )
