"""
acwa.yaw.max_power.complete_fits

Perform all the fits (i.e. for all time limits) for max power misallignment
"""

import pandas as pd 

import acwa.db as db

from acwa.tables import MaxPowerMisallignmentSchema
from acwa.yaw.max_power.fit import obtain_max_power_misallignment
from acwa.yaw.max_power.time_limits import define_max_power_misallignement_time_limits


def fit_all_time_limits_max_power_misallignments(
        df: pd.DataFrame,
        config_db: dict,
        data_type: str,
        year_offset: bool = False
):
    """
    Fit the max power misallignment for all time limits that we define, and 
    write the result into the database

    Args:
        df (pd.DataFrame): Datapoints (can be 10min or 1min)
        config_db (dict): Database configuration
        data_type (str): '10min' or '1min'
        year_offset (bool, optional): If True, move the present to 2023 to work
            with a mockup of 2023 data. Defaults to False
    """
    
    lst_time_limits = define_max_power_misallignement_time_limits(year_offset = year_offset)

    lst_dfs = []
    for time_limit in lst_time_limits:
        lst_dfs.append(
            obtain_max_power_misallignment(
                df, **time_limit)
        )
    df_max = pd.concat(lst_dfs)

    MaxPowerMisallignmentSchema.validate(df_max)
    table_name = 'max_power_misallignment' if data_type == '10min' else f'max_power_misallignment_{data_type}'

    db.write_df_as_table(
        df_max, config_db, 'vis', table_name, 
        index=False, if_exists='replace')
