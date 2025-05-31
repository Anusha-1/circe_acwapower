"""
acwa.data.read_input_tower_xy

Module to read input tower acceleration data
"""

import pandas as pd

import acwa.db as db

from acwa.data.datetime import transform_to_datetime

def read_input_tower_xy_data(config_db: dict) -> pd.DataFrame:
    """
    Read input tower xy data

    Args:
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with 10-min data of tower acceletation
    """

    lst_ids = ['id_wf', 'id_wtg', 'id_wtg_complete', 'timestamp']
    lst_var = [
        'toweracc_x_direction_avgxacc',
        'toweracc_x_direction_maxxacc',
        'toweracc_x_direction_minxacc',
        'toweracc_x_direction_stdxacc',
        'toweracc_y_direction_avgyacc',
        'toweracc_y_direction_maxyacc',
        'toweracc_y_direction_minyacc',
        'toweracc_y_direction_stdyacc',
        ]
    
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
