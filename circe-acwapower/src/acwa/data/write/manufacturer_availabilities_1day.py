"""
acwa.data.write.manufacturer_availabilities_1day

Write manufacturer_availabilities_1day
"""

import pandas as pd

from acwa.db import write_df_as_table
from acwa.tables import ManufacturerAvailabilities1DaySchema

def write_manufacturer_availabilities_1day(
        df: pd.DataFrame,
        config_db: dict
): 
    """
    Write the table manufacturer_availabilities_1day

    Args:
        df (pd.DataFrame): Dataframe with table data
        config_db (dict): Database configuration
    """
    
    output_table_name = "manufacturer_availabilities_1day"
    output_schema = "vis"

    df = df[ManufacturerAvailabilities1DaySchema.to_schema().columns.keys()]
    ManufacturerAvailabilities1DaySchema.validate(df)

    write_df_as_table(
        df,
        config_db,
        output_schema,
        output_table_name,
        if_exists="replace",
        index=False
    )