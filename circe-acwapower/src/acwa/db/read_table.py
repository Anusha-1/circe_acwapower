"""
acwa.db.read_table

Methods to read tables
"""

import logging

import pandas as pd

from .connect import connect_to_db
from .format import format_table_name

def read_table_as_df(
        name: str,
        config: dict,
        schema: str,
        verbose: bool = False,
        **kwargs
) -> pd.DataFrame:
    """
    Read SQL table as pandas Dataframe

    Args:
        name (str): Table name
        config (dict): config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml
        schema (str): Schema
        verbose (bool, optional): When using chunksize, logs the counter of chunks.
            Defaults to False
        **kwargs: Keyword arguments of pandas.read_sql_table 
            (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_table.html)

    Returns:
        pd.DataFrame: Table Data 
    """

    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    engine = connect_to_db(config)
    table_name = format_table_name(
        name, # Table name
        config, 
        schema # Schema
    )
    schema = schema if config['type'] == 'Azure' else None

    if 'chunksize' in kwargs.keys():
        df_generator = pd.read_sql_table(
            table_name, engine, schema = schema, **kwargs)
        full_df = pd.DataFrame()
        counter = 0
        for df in df_generator:
            counter += 1
            full_df = pd.concat([full_df, df])
            if verbose:
                logging.info(f"Read chunk {counter}")
        return full_df

    return pd.read_sql_table(
            table_name, engine, schema = schema, **kwargs)