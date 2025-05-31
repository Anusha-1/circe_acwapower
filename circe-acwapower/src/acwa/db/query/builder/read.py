"""
acwa.db.query.read

Module to read SQL queries
"""

import logging
import os
import pathlib

from sqlalchemy import text

def read_query(
        query_name: str,
        config: dict,
        queries_root_path: os.PathLike
) -> str:
    """Reads query from file

    Args:
        query_name (str): Name of the query file (without extension)
        config (dict): Configuration of database (i.e. "db" section)
        queries_root_path (os.PathLike): Folder where the queries are 
            saved.

    Returns:
        str: Query
    """
    
    path_to_query = pathlib.Path(
        queries_root_path,
        config["type"].lower(),
        f"{query_name}.sql"
    )
    with open(path_to_query, "r") as file:
        query = text(file.read())

    logging.info(f"Query: {query}")
    return query
