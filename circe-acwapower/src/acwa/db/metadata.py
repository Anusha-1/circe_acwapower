"""
acwa.db.metadata

Module to update metadata table
"""

from datetime import datetime
import logging

import pandas as pd
from retry import retry

from acwa.tables import MetadataSchema
from acwa.error import DatabaseError

from .check import check_table
from .connect import connect_to_db
from .format import format_table_name

@retry(DatabaseError, tries=10, delay=5)
def update_metadata_table(table_name: str, config: dict, schema: str) -> None:
    """
    Updates the metadata table (i.e. a table that informs about the updates of
    each other table)

    Args:
        table_name (str): Name of the updated table
        config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml
        schema (str): Schema of the updated table
    """

    engine = connect_to_db(config)
    metadata_table_name = format_table_name(
        "metadata", # Table name
        config, 
        "intermediate" # Schema
    )
    schema_metadata = "intermediate" if config['type'] == 'Azure' else None

    with engine.connect() as con:

        trans = con.begin()

        try:
            if check_table("metadata", config, "intermediate"):         
                df: pd.DataFrame = pd.read_sql_table(
                    metadata_table_name, engine, schema = schema_metadata)

                condition = ((df['schema']==schema) & (df['table']==table_name))
                if condition.any():
                    df.loc[condition,"last_update"] = datetime.now()
                else:
                    df = df._append({
                        "schema": schema,
                        "table": table_name,
                        "last_update": datetime.now()
                    }, ignore_index=True)
            
            else:
                ## Create a new table with one row
                record = {
                    "schema": schema,
                    "table": table_name,
                    "last_update": datetime.now()
                }
                df = pd.DataFrame.from_records([record])
            
            MetadataSchema.validate(df)
            df.to_sql(
                metadata_table_name, 
                con=engine, 
                schema=schema_metadata, 
                index=False, 
                if_exists="replace")
            
            trans.commit()
        
        except Exception as error:

            trans.rollback()
            logging.error(f"Error: {error}") # Re-try ?
            raise DatabaseError(
                "updating metadata table",
                error
            )
