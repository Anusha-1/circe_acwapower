"""
acwa.db.check

Checks for database
"""

import sqlalchemy

from .connect import connect_to_db
from .format import format_table_name

def check_table(name: str, config: dict, schema: str) -> bool:
    """
    Checks if a table exists in a certain schema

    Args:
        name (str): Name of the table
        config (dict): Database configuration (i.e. section "db")
        schema (str): Schema

    Raises:
        NotImplementedError: If the check has not been implemented for a db type
            it raises this error. Available types are: SQLite

    Returns:
        bool: True if table exists, False otherwise
    """

    engine = connect_to_db(config)
    formatted_name = format_table_name(name, config, schema)

    if config["type"] == "SQLite":
        return sqlalchemy.inspect(engine).has_table(formatted_name)
    elif config["type"] == "Azure":
        return sqlalchemy.inspect(engine).has_table(
            formatted_name, schema = schema)
        
    raise NotImplementedError(f"{config['type']} not implemented")
