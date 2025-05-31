"""
acwa.data.write.power_curves

Write power curves 
"""

import pandas as pd

from acwa.db import write_df_as_table #,read_table_as_df
from acwa.tables import interpolPCConfigSchema

def write_interpolated_power_curves(
        df_interpol: pd.DataFrame, 
        config_db: dict, 
        output_table_name: str = "interpolated_power_curves"):
    """
    Write table with power curves

    Args:
        df_pc (pd.DataFrame): Power curves
        config_db (dict): Configuration of database
        output_table_name (str, optional): Name of output table. Defaults to
            "interpolated_power_curves"
    """

    # # Load full
    # df_pc_old = read_table_as_df(
    #     "power_curves",
    #     config_db,
    #     "vis"
    # )

    # # Remove data from the pc_ids we have
    # df_pc_old = df_pc_old[~df_pc_old['pc_id'].isin(set(df_pc['pc_id']))]

    # # Concat
    # df_pc = pd.concat([df_pc, df_pc_old])

    # Check format
    df_interpol = df_interpol[interpolPCConfigSchema.to_schema().columns.keys()] 
    interpolPCConfigSchema.validate(df_interpol)

    # Write with replace
    write_df_as_table(
        df_interpol,
        config_db,
        "vis",
        output_table_name,
        index=False,
        if_exists="replace",
        chunksize=10000)
