"""
acwa.data.read_input_pitch

Module to read input pitch data
"""

import pandas as pd

import acwa.db as db

from acwa.data.datetime import transform_to_datetime

def read_input_pitch_data(incremental: bool, config_db: dict) -> pd.DataFrame:
    """
    Read input 10 min data

    Args:
        incremental (bool): If True, only reads data that has not been processed
            in oper_10min
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with 10-min data of pitch angles
    """

    lst_ids = ['id_wf', 'id_wtg', 'id_wtg_complete', 'timestamp']
    lst_var = [
        'blds_bladea_blpitchangle_max',
        'blds_bladea_blpitchangle_min',
        'blds_bladea_blpitchangle_std',
        'blds_bladea_blpitchangle_avg',
        'blds_bladeb_blpitchangle_max',
        'blds_bladeb_blpitchangle_min',
        'blds_bladeb_blpitchangle_std',
        'blds_bladeb_blpitchangle_avg',
        'blds_bladec_blpitchangle_max',
        'blds_bladec_blpitchangle_min',
        'blds_bladec_blpitchangle_std',
        'blds_bladec_blpitchangle_avg',
        'rotor_rpm', # To calculate lambda
        'wind_speed', # To calculate lambda
        ]

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
