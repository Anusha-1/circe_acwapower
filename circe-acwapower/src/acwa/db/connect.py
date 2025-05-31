"""
acwa.db.connect

Module to connect to database and tables
"""

import urllib
import urllib.parse

import sqlalchemy

def connect_to_db(config: dict) -> sqlalchemy.Engine:
    """
    Create connection to database

    Args:
        config (dict): Dictionary with database configuration options, i.e. db
            section of config/main.yml

    Raises:
        NotImplementedError: If the check has not been implemented for a db type
            it raises this error. Available types are: SQLite

    Returns:
        sqlalchemy.Engine: Engine object with connection to db
    """

    if config["type"] == "SQLite":
        engine = sqlalchemy.create_engine(config["path"])
    elif config["type"] == "Azure":

        server   = config['server']
        database = config['database']
        username = config['user']
        password = config['password']  
        driver   = '{ODBC Driver 18 for SQL Server}'

        conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
        Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

        params = urllib.parse.quote_plus(conn)
        conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

        engine = sqlalchemy.create_engine(conn_str, echo=True)

    else:
        raise NotImplementedError(f"{config['type']} not implemented")
       
    return engine
 