"""
acwa.data.read.reliability_input

Module to read and prepare data for reliability calculations
"""

from datetime import datetime
import logging

import pandas as pd

from acwa.db import read_table_as_df, run_query

def obtain_reliability_input(
        config_db: dict,  
        start_date: datetime | None = None,
        end_date: datetime | None = None,       
        incremental: bool = False,
         ) -> pd.DataFrame:
    """
    Reads 10-min data and prepare it for reliability model fitting or predicting
    It needs to merge the data with wtg_config to obtain the groups of each
    turbine, as the models are group-wise

    Args:
        config_db (dict): Configuration of database 
        start_datetime (datetime | None, optional): Start datetime. 
            Defaults to None
        end_datetime (datetime | None, optional): End datetime. 
            Defaults to None       
        incremental (bool, optional): Incremental flag. Defaults to False
        
    Returns:
        (pd.DataFrame): Formatted data
    """

    logging.info("Load WTG Config")
    df_wtg_config = read_table_as_df("wtg_config", config_db, "vis")

    logging.info("Load Basic 10-min data")
    if not incremental:
        df_data = read_table_as_df(
            "basic_10min", config_db, "intermediate",
            chunksize=10000, verbose=True)
        
        if start_date is not None and end_date is not None:
            df_data = df_data[(df_data['timestamp'] >= start_date) & (df_data['timestamp'] <= end_date)]
        # Note: We could introduce the time period directly in a SQL query...
    else:
        df_data: pd.DataFrame = run_query(
            "select_incremental_10min_basic_reliability",
            config_db,
            returns="Dataframe"
        )   

        if not df_data['timestamp'].dtype == 'datetime64[ns]':
            df_data['timestamp'] = pd.to_datetime(df_data['timestamp'])   

    # Merge data with wtg config to obtain the group of each turbine
    # Models are fitted at a group level
    logging.info("Merge data")
    df_data = df_wtg_config[['id_wtg_complete', 'id_group_complete','met_mast_id']].merge(
        df_data, how='right', on='id_wtg_complete'
    )
    df_data = df_data.rename(columns={'temperature':'ambient_temperature'})

    return df_data
