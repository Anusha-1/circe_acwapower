"""
acwa.data.compilation.max_datetime

Module to obtain the maximum datetime at a table
"""

from datetime import datetime

import pytz

import acwa.db as db

def extract_maximum_datetime(
        config_db: dict,
        id: str,
        data_type: str = '10min'
) -> datetime:
    """
    Select maximum datetime in a table by wind farm.

    NOTE: Hard-coded only for intermediate.input_10min

    Args:
        config_db (dict): Configuration of the database
        id (str): ID of the WF or Met-Mast
        data_type (str, optional): Data type. Options are '10min', '1min', 'met_mast'. 
            Defaults to '10min'

    Returns:
        datetime: Maximum datetime present in the table for that wind farm
    """

    utc = pytz.timezone('UTC')    

    query_dict = {
        "10min": "max_datetime_input_10min",
        "1min" : "max_datetime_input_1min",
        "met_mast": "max_datetime_input_met_mast"
    }

    if data_type in ["10min", "1min"]:
        params={"wind_farm_id": id}
    elif data_type in ["met_mast"]:
        params={"met_mast_id": id}

    max_datetime = db.run_query(
        query_dict[data_type], ## Maybe we could build the query directly, using the table name as input? Or generalize in another way
        config_db,
        params=params,
        returns="Fetchall"
    )[0][0]

    if max_datetime is not None:
        if config_db["type"] == 'SQLite':
            max_datetime = utc.localize(
                datetime.strptime(max_datetime, "%Y-%m-%d %H:%M:%S.%f")) # Time in UTC
        else:
            max_datetime = utc.localize(max_datetime) # Time in UTC

    return max_datetime
