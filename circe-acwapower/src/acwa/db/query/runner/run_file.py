"""
acwa.db.query.run

Run SQL query
"""

import os
from typing import Any

from ..builder.read import read_query
from .run import run_query_from_text

def run_query(
        query_name: str,
        config: dict,
        queries_root_path: os.PathLike = "queries",
        params: dict[str] = {},
        returns: str = "None",
        chunksize: int | None = None
) -> Any:
    """
    Run a query, that we have written into a file

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
        chunksize (int | None, optional): Chunksize to use. If None it does not 
            use chunksize. Defaults to None

    Returns:
        Any: Result
    """

    # Read the query
    query = read_query(query_name, config, queries_root_path)

    return run_query_from_text(
        query, config, params, returns, chunksize
    )
