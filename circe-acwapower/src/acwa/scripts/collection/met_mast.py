"""
acwa.scripts.collection.met_mast

Script to collect the met mast raw data
"""

import logging

import pandas as pd

import acwa.data as data
import acwa.db as db

from acwa.config import read_config
from acwa.log import format_basic_logging

def main(incremental=True):
    """
    Compilate and standarize 10min data

    Args:
        incremental (bool, optional): If True, loads only new data. If False,
            loads all. Defaults to True.
    """

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("------------ START SCRIPT: collection.met_mast ---------------")

    output_table_name = "oper_met_mast"
    output_schema = "vis"

    logging.info("Load the mapping information")
    df_map, df_var = data.load_mapping_information(config['db'], "met_mast")

    logging.info("Load Met Mast configuration")
    df_met_mast = db.read_table_as_df("met_mast_metadata", config["db"], "vis")
    df_wf = db.read_table_as_df("wf_config", config["db"], "vis")
    df_met_mast = df_met_mast.merge(
        df_wf[['wf_name', 'tz_data']], on="wf_name", how='left')

    for i, row in df_met_mast.iterrows():

        id_mm = row["met_mast_id"]
        wf_name = row["wf_name"]
        timezone = row["tz_data"]
        logging.info(f"Extracting data for Met Mast {id_mm}")

        df_map_mm = df_map[df_map["id"] == id_mm]

        logging.info("Check incremental flag")
        replace_flag = data.obtain_replace_flag(
            output_table_name, config["db"], output_schema, incremental, id_mm, 
            i, data_type="met_mast"
        )
        
        logging.info("Extract time horizon")
        max_datetime = (
            data.extract_maximum_datetime(config["db"], id_mm, data_type="met_mast")
            if not replace_flag
            else None
        )

        logging.info("Check input tables")
        lst_tables = list(set(df_map_mm['origin_table']))

        lst_dfs = []
        for table in lst_tables:
        
            logging.info(f"Extracting data for table {table}")
            df_map_mm_table = df_map_mm[df_map_mm['origin_table']==table]

            logging.info("Extracting raw table")
            df_data = data.extract_raw_data(
                wf_name, config['db'], max_datetime, timezone, table)
            
            logging.info("Map variables")
            df_data = data.DICT_MAP_MM[table](
                df_data, id_mm, df_map_mm_table, wf_name)

            logging.info("Set indices")
            df_data = df_data.set_index(
                ['wf_name', 'met_mast_id', 'timestamp', 'type'])
           
            lst_dfs.append(df_data)

        logging.info("Merging dataframes")
        df_data_mm = pd.concat(lst_dfs, axis = 1)

        logging.info("Checking missing columns")
        df_data_mm = data.complete_missing_signals(df_data_mm, df_var)

        logging.info("Writing to table")
        df_data_mm = df_data_mm.sort_index(axis=1)
        db.write_df_as_table(
            df_data_mm,                
            config['db'],
            output_schema,
            output_table_name,
            chunksize=10000,
            if_exists = "replace" if replace_flag else "append"
        )

if __name__ == "__main__":
    main(incremental=False)
