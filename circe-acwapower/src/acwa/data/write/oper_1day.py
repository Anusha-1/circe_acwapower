"""
acwa.data.write.oper_1day

Module to write vis.oper_1day
"""

import pandas as pd

from acwa.db import write_df_as_table
from acwa.tables import Oper1DaySchema

def write_oper_1day(
        df: pd.DataFrame,
        config_db: dict
):
    """
    Write oper_1day table

    Args:
        df (pd.DataFrame): Dataframe with table data
        config_db (dict): Database configuration
    """
    
    output_table_name = "oper_1day"
    output_schema = "vis"

    df = df[Oper1DaySchema.to_schema().columns.keys()]
    Oper1DaySchema.validate(df)
    
    write_df_as_table(
        df,
        config_db,
        output_schema,
        output_table_name,
        if_exists="replace",
        index=False
    )
