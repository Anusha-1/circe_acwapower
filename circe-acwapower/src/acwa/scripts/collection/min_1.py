"""
acwa.scripts.collection.min_1

Script to collect the raw data (1 min) of the wind farms, into a general table
"""

import logging

import pandas as pd

import acwa.data as data
import acwa.db as db

from acwa.config import read_config
from acwa.log import format_basic_logging

def main(incremental=True):
    """
    Compilate and standarize 1min data

    NOTE: Logic is completely identical to acwa.scripts.collection.min_10.
    Consider making a unique general function

    Args:
        incremental (bool, optional): If True, loads only new data. If False,
            loads all. Defaults to True.
    """

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("------------ START SCRIPT: collection.min_1 ----------------")

    output_table_name = "input_1min"
    output_schema = "intermediate"

    logging.info("Load the mapping information")
    df_map, df_var = data.load_mapping_information(config['db'], "1min")

    logging.info("Load wind farms configuration")
    df_wf = db.read_table_as_df("wf_config", config["db"], "vis")

    for i, row in df_wf.iterrows():
        id_wf = row["id_wf"]
        wf_name = row["wf_name"]
        timezone = row["tz_data"]
        logging.info(f"Extracting 1-min signals for Wind Farm {wf_name}")

        df_map_wf = df_map[df_map["id"] == id_wf]

        logging.info("Check incremental flag")
        replace_flag = data.obtain_replace_flag(
            output_table_name, config["db"], output_schema, incremental, id_wf, 
            i, data_type="1min"
        )

        logging.info("Extract time horizon")
        max_datetime = (
            data.extract_maximum_datetime(config["db"], id_wf, data_type="1min")
            if not replace_flag
            else None
        )

        logging.info("Check input tables")
        lst_tables = list(set(df_map_wf['origin_table']))

        lst_dfs = []
        for table in lst_tables:

            logging.info(f"Extracting data for table {table}")
            df_map_wf_table = df_map_wf[df_map_wf['origin_table']==table]

            logging.info("Extracting raw table")
            df_data = data.extract_raw_data(
                wf_name, config['db'], max_datetime, timezone, table)
            
            logging.info("Map variables")          
            df_data = data.DICT_MAP_1MIN[table](
                df_data, id_wf, df_map_wf_table)
            
            logging.info("Set indices")
            df_data = df_data.set_index(
                ['id_wf', 'id_wtg', 'id_wtg_complete', 'timestamp'])

            lst_dfs.append(df_data)

        logging.info("Merging dataframes")
        df_data_wf = pd.concat(lst_dfs, axis = 1)

        logging.info("Checking missing columns")
        df_data_wf = data.complete_missing_signals(df_data_wf, df_var)

        logging.info("Writing to table")
        df_data_wf = df_data_wf.sort_index(axis=1)
        db.write_df_as_table(
            df_data_wf,                
            config['db'],
            output_schema,
            output_table_name,
            chunksize=10000,
            if_exists = "replace" if replace_flag else "append"
        )

    logging.info("----------------------- FINISH -----------------------------")


if __name__ == "__main__":
    main(incremental=False)
