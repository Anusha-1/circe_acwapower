"""
acwa.db.format

Module to format SQL names
"""

def format_table_name(name: str, config: dict, schema: str) -> str:
    """
    Format table name depending on type of SQL

    Args:
        name (str): Name of the table
        config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml
        schema (str): Name of the schema

    Returns:
        str: Table name to use
    """

    if config["type"] == "SQLite":
        return f"{schema}.{name}"
    
    return name