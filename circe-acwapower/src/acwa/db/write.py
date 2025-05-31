"""
acwa.db.write

Functions to write in the database
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from retry import retry

if TYPE_CHECKING:
    import pandas as pd
    
from acwa.error import DatabaseError

from .format import format_table_name
from .connect import connect_to_db
from .metadata import update_metadata_table

def write_df_as_table(
        df: pd.DataFrame, 
        config: dict, 
        schema: str,
        name: str,
        **kwargs) -> None:
    """
    Function to write a database table from a pandas dataframe.

    Args:
        df (pd.DataFrame): Pandas dataframe to write as a SQL table
        config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml
        schema (str): Name of the schema
        name (str): Name of the table
        **kwargs: Additional kwargs are passed to the .to_sql method of pandas
            Dataframe (except schema)

    Raises:
        NotImplementedError: If the check has not been implemented for a db type
            it raises this error. Available types are: SQLite
    """

    write_df_as_table_without_update(
        df, config, schema, name, **kwargs
    )    
    
    update_metadata_table(name, config, schema)

@retry(DatabaseError, tries=10, delay=5)
def write_df_as_table_without_update(
        df: pd.DataFrame, 
        config: dict, 
        schema: str,
        name: str,
        **kwargs) -> None:
    """
    Function to write a database table from a pandas dataframe (without 
    updating the metadata table)

    Args:
        df (pd.DataFrame): Pandas dataframe to write as a SQL table
        config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml
        schema (str): Name of the schema
        name (str): Name of the table
        **kwargs: Additional kwargs are passed to the .to_sql method of pandas
            Dataframe (except schema)
    """

    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    engine = connect_to_db(config)
    formatted_name = format_table_name(name, config, schema)

    with engine.connect() as con:

        trans = con.begin()

        try:

            if config['type'] == 'SQLite':
                df.to_sql(formatted_name, con=engine, **kwargs)
            elif config['type'] == 'Azure':
                df.to_sql(formatted_name, con=engine, schema=schema, **kwargs)

            trans.commit()

        except Exception as error:

            trans.rollback()
            logging.error(f"Error: {error}")
            raise DatabaseError(
                f"writing table {schema}.{name}",
                error
            )
        