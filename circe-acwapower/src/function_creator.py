"""
function_creator

Script to create some SQL functions
"""

import logging
import pathlib

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main():
    
    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------- START SCRIPT: function_creator ---------------")

    logging.info("Reading variables")
    df_variables = read_table_as_df("variables", config['db'], "vis")
    
    logging.info("Creating intermediate functions to select timeseries")
    lst_tables = list(set(df_variables['table']))
    
    query_intro = """
    CREATE FUNCTION intermediate.extract_timeseries_{table}
    (
        @start_date DATE,
        @end_date DATE,
        @signal VARCHAR(MAX)
    )
    RETURNS TABLE
    AS
    RETURN
    (
        SELECT
            timestamp,  -- Marca de tiempo de cada lectura
            id_wtg_complete,  -- Identificador completo de la turbina eólica
            id_wf,
            CASE @signal"""
    
    query_outro = """
                ELSE NULL
            END AS value
        FROM vis.oper_10min
        WHERE timestamp BETWEEN @start_date AND @end_date
    )
    """    
    
    for table in lst_tables:
        logging.info(f"Creating query for table {table}")
        df_aux = df_variables[df_variables['table']==table]

        query = query_intro.format(table=table)

        for _, row in df_aux.iterrows():
            query += f"\n\t\t\t\tWHEN \'{row['variable']}\' THEN {row['variable_internal']}"

        query += query_outro

        file_path = pathlib.Path(
            "queries", "azure", "functions", f"extract_timeseries_{table}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wt", encoding="utf-8") as f:
            f.writelines(query)


if __name__ == '__main__':
    main()

