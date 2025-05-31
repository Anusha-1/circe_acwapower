"""
acwa.db.query.run

Run SQL query inside a transaction
"""

import logging
import os
from typing import Any

import pandas as pd
from retry import retry

from acwa.error import DatabaseError
from ..builder.read import read_query
from ...connect import connect_to_db

@retry(DatabaseError, tries=10, delay=5)
def run_query_in_transaction(
        query_name: str,
        config: dict,
        queries_root_path: os.PathLike = "queries",
        params: dict[str] = {},
        returns: str = "None"
) -> Any:
    """
    Run a query, that we have written into a file, inside a transaction (so it 
    will rollback to the previous state when failing)

    Args:
        query_name (str): Name of the query file (without extension)
        config (dict): Configuration of database (i.e. "db" section)
        queries_root_path (os.PathLike, optional): Folder where the queries are 
            saved. Defaults to "queries".
        params (dict[str], optional): Parameters of the query. Keys sould have 
            the name that appear in the query file, and values should be the 
            value that we have to replace it with. Defaults to {}.
        returns (str): Type of object to return. Options are:

                - None: Returns None
                - Cursor: Returns cursor object
                - Fetchall: Returns cursor.fetchall()
                - Dataframe: Returns dataframe 

            Defaults to None

    Returns:
        Any: Result
    """

    # Read the query
    query = read_query(query_name, config, queries_root_path)

    # Run query
    engine = connect_to_db(config)
    with engine.connect() as con:
        trans = con.begin()
        try:
            result = con.execute(
                query, 
                params)
            trans.commit()

        except Exception as error:

            trans.rollback()
            logging.error(f"Error: {error}")
            raise DatabaseError(
                "query",
                error
            )
        
        if returns == 'None':
            obj_to_return = None
        elif returns == 'Cursor':
            obj_to_return = result
        elif returns == 'Fetchall':
            obj_to_return = result.fetchall()
        elif returns == 'Dataframe':
            obj_to_return = pd.DataFrame(result.fetchall(), columns=result.keys())
        
    return obj_to_return
