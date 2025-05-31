"""
acwa.db.query.builder.select_incremental

Query functions to read from a table incrementally
"""

from sqlalchemy import text, TextClause

def build_query_select_incremental(
        config_db: dict, 
        input_table_name: str,
        timestamp_col: str) -> TextClause:
    """
    Build a SQL query to select data from a table incrementally, i.e. starting
    from a specific time

    Args:
        config_db (dict): Database configuration
        input_table_name (str): Name of the table
        timestamp_col (str): Name of the timestamp column

    Returns:
        TextClause: Query to select data with a parameter :start to input the start
            datetime
    """
 

    if config_db["type"] == "Azure":        
        query = "SELECT * \n"
        query += f"FROM [raw].[{input_table_name}] t \n"
        query += f"WHERE t.{timestamp_col} > :start"
    elif config_db["type"] == "SQLite":
        query = "SELECT * \n"
        query += f"FROM \"raw.{input_table_name}\" t \n"
        query += f"WHERE t.{timestamp_col} > :start"
    
    return text(query)
