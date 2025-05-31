"""
acwa.data.read_input_10min

Module to read input 10min data
"""

import pandas as pd

import acwa.db as db

from acwa.data.datetime import transform_to_datetime


def read_input_10min_data(incremental: bool, config_db: dict) -> pd.DataFrame:
    """
    Read input 10 min data

    Args:
        incremental (bool): If True, only reads data that has not been processed
            in oper_10min
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with 10-min data
    """

    df_var = db.read_table_as_df("variables", config_db, "vis")
    
    lst_var = df_var[
        (df_var["variable_type"] == "essential")
        & (df_var["data_type"] == "10min")
    ]["variable_internal"].to_list()
    lst_ids = ['id_wf', 'id_wtg', 'id_wtg_complete', 'timestamp']

    if incremental:
        query = db.build_query_select_input_10min(config_db, lst_ids + lst_var)

        df: pd.DataFrame = db.run_query_from_text(
            query, config_db, returns="DataFrame"
        )
    else:
        df = db.read_table_as_df(
            "input_10min",
            config_db,
            "intermediate",
            columns=lst_ids + lst_var,
            chunksize=100000,
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
