"""
acwa.db.query.builder.select_input_10min

Query functions to select only essential columns from input 10min
"""

from sqlalchemy import text, TextClause


def build_query_select_input_10min(
        config_db: dict,
        lst_var: list[str]
) -> TextClause:
    """
    Build a query to select only selected variables from input_10min, beyond the
    current horizon of timestamps at basic_10min 

    Args:
        config_db (dict): Database configuration
        lst_var (list[str]): List of variable signals

    Raises:
        ValueError: If DB type is not recognized

    Returns:
        TextClause: Query to run 
    """
    
    if config_db['type'] == "Azure":
        query = "SELECT ",
        for var in lst_var:
            query += f"\t i.{var}, \n"
        query = query[:-3]
        query += "FROM intermediate.input_10min i\n"
        query += "JOIN intermediate.[10min_horizons_basic] h ON i.id_wtg_complete = h.id_wtg_complete\n"
        query += "WHERE i.timestamp > h.horizon_datetime;"

    elif config_db['type'] == "SQLite":
        query = "SELECT ",
        for var in lst_var:
            query += f"\t i.{var}, \n"
        query = query[:-3]
        query += "FROM \"intermediate.input_10min\" i\n"
        query += "JOIN \"intermediate.10min_horizons_basic\" h ON i.id_wtg_complete = h.id_wtg_complete\n"
        query += "WHERE i.timestamp > h.horizon_datetime;"
    
    else:
        raise ValueError(f"Unrecognized DB type {config_db['type']}")
    
    return text(query)
