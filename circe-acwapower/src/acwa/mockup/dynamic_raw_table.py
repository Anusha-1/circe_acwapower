"""
acwa.mockup.dynamic_raw_table

Module with function to create a dynamic raw table by using the data from the
static raw table
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import pytz

import pandas as pd

from acwa.config import read_config
from acwa.data import transform_to_datetime
from acwa.db import check_table, run_query,run_query_in_transaction, write_df_as_table

def write_dynamic_raw_table(
    input_query: str,
    output_table_name: str,
    month_period: int = 24,
    config: dict | None = None,
    timezone: str = 'UTC',
    timestamp_col: str = 'ttimestamp',
    timestamp_input_format: str = "%Y-%m-%d %H:%M:%S",
    now: datetime | None = None
) -> None:
    """
    Writes a dynamic raw input table. It starts from a static table of another
    year and will input the data of that table pretending that is the new
    current data

    Args:
        input_query (str): Collection of input queries to use
        output_table_name (str): Name of output table name
        month_period (int, optional): Period of months where data of dynamic 
            input will be available. Defaults to 24.
        config (dict | None, optional): Configuration options. If None, it will
            read the file. Defaults to None. 
        timezone (str, optional): Timezone of the timestamps of the data.
        timestamp_col (str, optional): Original timestamp column name.
        timestamp_input_format (str, optional): Expected format of input 
            timestamps. Defaults to "%Y-%m-%d %H:%M:%S"
        now (datetime | None, optional): Temporal limit to consider. 
            If None, obtain present moment from system. Defaults to None
    """
        
    if config is None:
        config = read_config()
    
    logging.info("Obtaining times")
    tz = pytz.timezone(timezone)
    now = now if now is not None else datetime.now()
    end_time = now.astimezone(tz) - relativedelta(year=2023)
    start_time = end_time - relativedelta(months=month_period)

    ## Step 1: Check if output table already exists
    check = check_table(output_table_name, config['db'], "raw")

    if check:

        logging.info("Dynamic table already exists")

        logging.info("Delete old entries")
        run_query_in_transaction(
            f"delete_{input_query}",
            config["db"],
            params = {
                "start": start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        result = run_query(
            f"max_datetime_{input_query}",
            config["db"],
            returns="Fetchall"
        )

        logging.info("Fetch result")
        if config['db']['type'] == 'SQLite':
            current_max_datetime = datetime.strptime(
                result[0][0],
                "%Y-%m-%d %H:%M:%S.%f")
        else:
            current_max_datetime = result[0][0]  

        start_time = current_max_datetime + timedelta(seconds=1)
        logging.info(f"Current max time in data: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        df: pd.DataFrame = run_query(
            f"read_static_{input_query}",
            config["db"],
            params = {
                "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
            },
            returns="Dataframe"
        )
        logging.info(f"Fetched {len(df)} rows")

        df = transform_to_datetime(
            df, 
            timestamp_col, 
            timestamp_input_format, 
            )

        logging.info("Writting in table")
        write_df_as_table(
            df,
            config['db'],
            "raw",
            output_table_name,
            if_exists='append',
            index=False
        )  
    
    else:        
        logging.info("Dynamic table doesn't exist")
        df = run_query(
            f"read_static_{input_query}",
            config["db"],
            params = {
                "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
            },
            returns="Dataframe",
            chunksize = 10000
        )

        df = transform_to_datetime(
            df, 
            timestamp_col, 
            timestamp_input_format, ## Does this work at SQLite and Azure?
            )  

        logging.info("Writting in table")
        write_df_as_table(
            df,
            config['db'],
            "raw",
            output_table_name,
            index=False,
            chunksize=10000
        )
