"""
acwa.scripts.collection.alarms

Script to collect the raw alarms of the wind farms, into a general table
"""

import logging

import acwa.data as data

from acwa.config import read_config
from acwa.db import (
    read_table_as_df, 
    check_table, 
    run_query)
from acwa.log import format_basic_logging

def main(incremental = True):
    """
    Compilate and standarize alamrs

    Args:
        incremental (bool, optional): If True, loads only new data. If False,
            loads all. Defaults to True.
    """

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------ START SCRIPT: collection.alarms ---------------")

    output_table_name = "input_alarms"
    output_schema = 'intermediate'

    logging.info("Load WF Configuration")
    df_wf_config = read_table_as_df("wf_config", config['db'], 'vis')

    logging.info("Initializing loop in wind farms")
    for i, row in df_wf_config.iterrows():

        try:

            wf_name = row['wf_name']
            id_wf = row['id_wf']
            timezone = row['tz_alarms']
            logging.info(f"Collecting data from wind farm {wf_name} (id: {id_wf})")

            logging.info(f"Checking if table {output_table_name} exists")
            check = check_table(output_table_name, config['db'], output_schema)

            if check and incremental:

                logging.info("Table exists. Checking if it contains data from this wind farm")            
                df_existing_ids = run_query(
                    "select_distinct_wf_in_alarms",
                    config['db'],
                    returns="Dataframe"
                )
                check_wind_farm = id_wf in list(df_existing_ids['id_wf'])

                if check_wind_farm:
                    logging.info("Wind farm exists.")  
                    data.update_input_alarms(config['db'], id_wf, wf_name, timezone)

                else:

                    logging.info("Wind farm does not exist. Reading the whole data set")
                    data.append_new_alarms(config['db'], id_wf, wf_name, timezone)
            
            else:

                logging.info("Table does not exist. Reading the whole data set")
                data.append_new_alarms(
                    config['db'], id_wf, wf_name, timezone, if_exists="replace")

                incremental = True # After creating the new table, we change the flag
                                    # At next iterations, it will detect that the
                                    # new wind farms don't exist in table.
        except Exception as error:
            logging.error(f"Unable to collect data for {wf_name}: {error}")

    logging.info("---------------------- FINISH ------------------------------")


if __name__ == '__main__':
    main(incremental=False)
