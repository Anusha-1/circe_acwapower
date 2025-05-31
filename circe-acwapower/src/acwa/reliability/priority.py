"""
acwa.reliability.priority

Establish priority in reliability models
"""

from datetime import datetime

import pandas as pd

from acwa.db import check_table, read_table_as_df
from acwa.tables import ReliabilityModelsSchema

def establish_priority(
        df_full_index: pd.DataFrame,
        config_db: dict
) -> pd.DataFrame:
    """
    Establish priority

    Args:
        df_full_index (pd.DataFrame): Dataframe with all models combination
        config_db (dict): Configuration of database

    Raises:
        NotImplementedError: If table exists, not implemented

    Returns:
        pd.DataFrame: Dataframe with all models, in the order to fit
    """

    default_date = datetime(year=2000, month=1, day=1)

    if check_table("reliability_models", config_db, "intermediate"):
        df_current_index = read_table_as_df(
            "reliability_models", config_db, "intermediate"
        )

        df_full_index = df_full_index.merge(
            df_current_index,
            on = ['signal', 'group', 'oper_stat', 'quantile'],
            how = 'left'
        )
        df_full_index['last_update'] = df_full_index['last_update']\
            .fillna(default_date)
  
    else:
        df_full_index['last_update'] = default_date

    ReliabilityModelsSchema.validate(df_full_index)

    return df_full_index.sort_values(
        by=['last_update','signal','group','oper_stat'])
