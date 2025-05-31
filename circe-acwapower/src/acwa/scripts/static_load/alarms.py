"""
acwa.scripts.static_load.alarms

Script to create raw static table with alarms
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import list_files_in_path, read_excel
from acwa.log import format_basic_logging

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("-------------- START SCRIPT: static_load.pitch -------------")

    logging.info("Read input files and build dataframe")
    list_files = list_files_in_path(
        pathlib.Path("input", "alarms"),
        config['file_storage'],
        'data'
    )
    list_dfs = []
    list_columns = [
        "Unit", "Serial no.", "Code", "Description", "Detected", "Device ack.",
        "Reset/Run", "Duration", "Event type", "Severity", "Remark"]
    for file in list_files:
        df_aux = read_excel(
            file,
            config['file_storage'],
            'data')
        list_dfs.append(df_aux[list_columns])
    df = pd.concat(list_dfs)

    logging.info("Transforming columns to datetime")
    for col in ["Detected", "Device ack.", "Reset/Run"]:
        df[col] = pd.to_datetime(
            df[col].apply(lambda x: x[:-4]), 
            format="%d/%m/%Y %H:%M:%S")

    logging.info("Write table raw.static_alarms_Khalladi")
    write_df_as_table(
        df,
        config['db'],
        "raw",
        "static_alarms_Khalladi",
        if_exists = "replace",
        index = False
    )

    logging.info("Write table raw.static_alarms_Azerbaijan (with the same alarmas as Khalladi)")
    lst_dummy_wtgs = ['WTG01', 'WTG02', 'WTG03', 'WTG04', 'WTG05', 'WTG06', 
                      'WTG07', 'WTG08', 'WTG09', 'WTG10', 'WTG11']
    df = df[df['Unit'].isin(lst_dummy_wtgs)]
    write_df_as_table(
        df,
        config['db'],
        "raw",
        "static_alarms_Azerbaijan",
        if_exists = "replace",
        index = False
    )

if __name__ == "__main__":
    main()
