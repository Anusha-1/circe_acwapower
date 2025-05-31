"""
acwa.data.compilation.append_new_10min

Module to append a new wind farm on input 10min
"""

import logging
import pytz


from acwa.db import read_table_as_df, write_df_as_table

from .mapping import DICT_MAP_ALARMS
from ..datetime import transform_timezone

def append_new_alarms(
        config_db: dict,
        id_wf: int,
        wf_name: str,
        timezone: str,
        if_exists: str = 'append'
):
    """
    Append a new wind farm on the table intermediate.input_alarms.

    Args:
        config_db (dict): Database configuration
        id_wf (int): Id of wind farm
        wf_name (str): Name of wind farm
        timezone (str): Timezone
        if_exists (str, optional): if_exists kwarg of write table. Defaults to
            "append" 
    """

    output_table_name = "input_alarms"
    output_schema = 'intermediate'

    # Timezones
    utc = pytz.timezone('UTC')
    data_tz = pytz.timezone(timezone)

    input_table_name = f"realtime_alarms_{wf_name}"
    df = read_table_as_df(
        input_table_name,
        config_db,
        "raw",
    )

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
        chunksize=100000,
        if_exists = if_exists
    )
