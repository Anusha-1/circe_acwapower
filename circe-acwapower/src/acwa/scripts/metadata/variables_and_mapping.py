"""
acwa.scripts.metadata.variables_and_mapping

Script to upload the variables and mapping metadata tables
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.files import read_excel
from acwa.log import format_basic_logging

def main():


    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------- START SCRIPT: metadata.variables_and_mapping -------")

    input_file_path = pathlib.Path('input', 'variables', 'variable_list.xlsx')

    logging.info("Writing General List of Variables")
    df = read_excel(
        input_file_path,
        config['file_storage'],
        'data',
        sheet_name = 'General Variable List'
    )
    write_df_as_table(df, config['db'], "vis", "variables",
                      if_exists="replace", index=False)

    logging.info("Reading WF info")
    df_wf = read_table_as_df("wf_config", config['db'], "vis")

    lst_df_maps = []
    for _,row in df_wf.iterrows():

        logging.info(f"Reading mapping {row['wf_name']}")
        df_map = read_excel(
            input_file_path,
            config['file_storage'],
            'data',
            sheet_name = f'Mapping {row["wf_name"]}'
        )
        df_map['id'] = row["id_wf"]
        lst_df_maps.append(df_map)

    for _,row in df_wf.iterrows():

        logging.info(f"Reading mapping {row['wf_name']}")
        df_map = read_excel(
            input_file_path,
            config['file_storage'],
            'data',
            sheet_name = f'Mapping {row["wf_name"]} Met Mast'
        )
        df_map = df_map.rename(columns={"id_met_mast": "id"})
        lst_df_maps.append(df_map)
    
    logging.info("Writing complete mapping")
    df_map = pd.concat(lst_df_maps)
    write_df_as_table(df_map, config['db'], "vis", "mapping",
                      if_exists="replace", index=False)


if __name__ == "__main__":
    main()