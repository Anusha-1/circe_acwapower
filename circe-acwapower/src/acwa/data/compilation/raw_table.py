"""
acwa.data.compilation.raw_table

Module to extract info from raw tables
"""

from datetime import datetime

import pandas as pd
import pytz

import acwa.db as db

def extract_raw_data(
        wf_name: str, 
        config_db: dict, 
        max_datetime: datetime | None, 
        timezone: str,
        input_table_name: str,
) -> pd.DataFrame:
    """
    Extract the raw input from a table to recover signals

    Args:
        wf_name (str): Wind farm name
        config_db (dict): Database configuration
        max_datetime (datetime | None): Maximum datetime in already collected 
            data. If None, we assume that we need to extract all the available
            data.
        timezone (str): Timezone for the data values. MAYBE WE NEED TO HAVE THIS AT TABLE LEVEL...
        input_table_name (str): Table name with data to extract
        
    Returns:
        pd.DataFrame: Extracted dataframe
    """
   
    if max_datetime is not None:

        timestamp_col = "datetime" # Generalize this in metadata ?

        query = db.build_query_select_incremental(
            config_db, input_table_name, timestamp_col
        )
   
        data_tz = pytz.timezone(timezone)

        df = db.run_query_from_text(
            query, config_db, 
            params = {"start": max_datetime.astimezone(data_tz)},
            returns = "Dataframe",
            chunksize = 10000
        )     

    else:
        df = db.read_table_as_df(
            input_table_name,
            config_db,
            "raw",
        ) 

    return df
