"""
acwa.data.write.reliability

Module to write intermediate.reliability_ts
"""

import pandas as pd

from acwa.db import write_df_as_table

def write_reliability_ts(
        df_rel: pd.DataFrame,
        incremental: bool,
        config_db: dict
):
    """
    Write the table intermediate.reliability_ts

    Args:
        df_rel (pd.DataFrame): Dataframe with reliability time series
        incremental (bool): Incremental flag
        config_db (dict): Configuration of database
    """
    
    output_table_name = 'reliability_ts'
    output_schema = 'intermediate'

    if incremental:
        write_df_as_table(
            df_rel,
            config_db,
            output_schema,
            output_table_name,
            if_exists='append',
            index=False
        )
    else:
        write_df_as_table(
            df_rel,
            config_db,
            output_schema,
            output_table_name,
            if_exists='replace',
            index=False
        )