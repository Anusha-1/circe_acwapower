"""
acwa.scripts.static_load.pitch

Script to upload the pitch angle data to a static table
"""

import logging
import pathlib

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_excel
from acwa.log import format_basic_logging

def main(lst_wf: list[str] = ['Khalladi','Azerbaijan']):
    """
    Loads the tower acceleration data into static data tables

    Args:
        lst_wf (list[str], optional): List of WFs to load. 
            Defaults to ['Khalladi','Azerbaijan'].
    """

    # Configuration and logger
    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------- START SCRIPT: static_load.tower_acceleration --------------")

    if 'Khalladi' in lst_wf:

        logging.info("Loading Khalladi tower acceleration")
        input_path = pathlib.Path(
            "input", 
            "Historical data", 
            "TowXY.xlsx")

        df = read_excel(input_path, config['file_storage'], container='data')
        
        logging.info("writting Khalladi tower acceleration")
        write_df_as_table(
            df,
            config['db'],
            "raw",
            "static_tower_acceleration_Khalladi",
            index=False,
            if_exists="replace",
            chunksize=10000
        )

    if "Azerbaijan" in lst_wf:

        logging.info("Loading Azerbaijan tower acceleration")

        ## Filter to first 11 turbines
        df = df.filter(regex="(WTG(0.*|10.*|11.*)|PCTimeStamp)")

        logging.info("writting Azerbaijan tower acceleration")
        write_df_as_table(
            df,
            config['db'],
            "raw",
            "static_tower_acceleration_Azerbaijan",
            index=False,
            if_exists="replace",
            chunksize=10000
        )    

    logging.info("---------------------- FINISH ------------------------------")

if __name__ == '__main__':
    main()