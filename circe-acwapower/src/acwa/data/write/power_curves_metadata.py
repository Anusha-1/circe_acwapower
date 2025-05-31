"""
acwa.data.write.power_curves_metadata

Write power curves metadata
"""

import pandas as pd

from acwa.db import read_table_as_df, write_df_as_table
from acwa.tables import PCMetadataSchema

def write_power_curves_metadata(
        df_pc_metadata: pd.DataFrame, 
        config_db: dict,
        output_table_name: str = "pc_metadata"):
    """
    Write table with power curves metadata

    Args:
        df_pc_metadata (pd.DataFrame): Power curves metadata
        config_db (dict): COnfiguration of database
        output_table_name (str, optional): Name of output table. Defaults to
            "pc_metadata"
    """

    # Load full
    df_pc_metadata_old = read_table_as_df(
        "pc_metadata",
        config_db,
        "vis"
    )

    # Remove data from the pc_ids we have
    df_pc_metadata_old = df_pc_metadata_old[~df_pc_metadata_old['pc_id'].isin(set(df_pc_metadata['pc_id']))]

    # Concat
    df_pc_metadata = pd.concat([df_pc_metadata, df_pc_metadata_old])

    # Check format
    df_pc_metadata = df_pc_metadata[PCMetadataSchema.to_schema().columns.keys()] 
    PCMetadataSchema.validate(df_pc_metadata)

    # Write with replace
    write_df_as_table(
        df_pc_metadata,
        config_db,
        "vis",
        output_table_name,
        index=False,
        if_exists="replace",
        chunksize=10000)
