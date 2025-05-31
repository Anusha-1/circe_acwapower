"""
acwa.db.query.runner.run

Module to run query from text
"""

from typing import Any

import pandas as pd
from sqlalchemy import TextClause

from ...connect import connect_to_db

def run_query_from_text(
        query: TextClause,
        config: dict,
        params: dict[str] = {},
        returns: str = "None",
        chunksize: int | None = None
) -> Any:
    """
    Run a query, that we have written into a file

    Args:
        query (TextClause): Query to run
        config (dict): Configuration of database (i.e. "db" section)
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
    
    engine = connect_to_db(config)
    with engine.connect() as con:
        result = con.execute(
            query, 
            params)
        
        if returns == 'None':
            obj_to_return = None
        elif returns == 'Cursor':
            obj_to_return = result
            con.commit()
        elif returns == 'Fetchall':
            obj_to_return = result.fetchall()
        elif returns == 'Dataframe':
            if chunksize is not None:
                chunks = []
                while True:
                    rows = result.fetchmany(chunksize)
                    if not rows:
                        break
                    df_chunk = pd.DataFrame(rows,columns=result.keys())
                    
                    chunks.append(df_chunk)
                obj_to_return = pd.concat(chunks, ignore_index=True)
            else:
                obj_to_return = pd.DataFrame(
                    result.fetchall(), columns=result.keys())        
        
    return obj_to_return
