"""
acwa.data.read.input_1min

Module to read input 1 min data
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd

from acwa.data.datetime import transform_to_datetime
from acwa.db import run_query, read_table_as_df


def read_input_1min_data(
    incremental: bool,
    config_db: dict,
    days_period: int | None = 60,
    year_offset: bool = False,
) -> pd.DataFrame:
    """
    Read input 10 min data

    Args:
        incremental (bool): If True, only reads data that has not been processed
            in oper_10min
        config_db (dict): Database configuration
        days_period (int, optional): Period (in months) of data to read.
            If None, there are no limiting period. Defaults to 3
        year_offset (bool, optional):  If True, put the present moment in 2023
            when retrieving data (True to work with mockup data in 2023, in
            production should work with False). Defaults to False

    Returns:
        pd.DataFrame: Dataframe with 1-min data
    """
    
    if days_period is not None: 
        time_limit = (
            datetime.now()
            - relativedelta(year=2023) * year_offset
            - timedelta(days=days_period)
        )
    else:
        time_limit = (
            datetime.now()
            - relativedelta(year=2023) * year_offset
            - timedelta(days=1000)
        )

    if incremental:

        df: pd.DataFrame = run_query(
            "select_incremental_1min",
            config_db,
            params={"time_limit": time_limit},
            returns="Dataframe",
        )
    else:
        if days_period is not None:
            df: pd.DataFrame = run_query(
                "select_incremental_1min_full",
                config_db,
                params={"time_limit": time_limit},
                returns="Dataframe",
            )
        else:
            df = read_table_as_df(
                "input_1min", config_db, "intermediate", chunksize=1000000, verbose = True
            )

    if config_db["type"] == "SQLite":
        df = transform_to_datetime(
            df,
            "timestamp",
            "%Y-%m-%d %H:%M:%S.%f",
            "timestamp",
            drop_original_col=False,
        )

    return df
