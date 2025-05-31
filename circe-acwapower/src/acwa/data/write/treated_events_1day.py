"""
acwa.data.write.treated_events_1day

Write treated_events_1day
"""

import pandas as pd

from acwa.db import write_df_as_table
from acwa.tables import TreatedEvents1DaySchema

def write_treated_events_1day(
        df: pd.DataFrame,
        config_db: dict
): 
    """
    Write the table treated_events_1day

    Args:
        df (pd.DataFrame): Dataframe with table data
        config_db (dict): Database configuration
    """
    
    output_table_name = "treated_events_1day"
    output_schema = "vis"

    df = df[TreatedEvents1DaySchema.to_schema().columns.keys()]
    TreatedEvents1DaySchema.validate(df)

    write_df_as_table(
        df,
        config_db,
        output_schema,
        output_table_name,
        if_exists="replace",
        index=False
    )