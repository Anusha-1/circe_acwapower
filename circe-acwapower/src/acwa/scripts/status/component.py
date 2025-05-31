"""
acwa.scripts.status.component

Script to retrieve the status by component
"""

from datetime import datetime
import logging

import acwa.alarms.component as comp
import acwa.db as db
import acwa.reliability as rel

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.tables import StatusComponentSchema

def main():

    start = datetime.now()

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("------------- START SCRIPT: status.component ---------------")

    # Step 1: Obtain component list
    # NOTE: Consider to upload a metadata table
    logging.info("Obtain component list")
    df_alarms_metadata = db.read_table_as_df(
        "alarms_metadata", config['db'], "vis")
    df_temp_signals = db.read_table_as_df(
        "temperature_signals", config['db'], "vis"
    )
    lst_components = comp.get_list_of_components(
        config["db"],
        df_alarms_metadata=df_alarms_metadata)

    # Step 2: Read last timestamp from status table
    logging.info("Reading status")
    df_status = db.read_table_as_df("status", config["db"], "vis")

    # Step 3: Read input alarms
    logging.info("Reading alarms")
    df_all_alarms = db.read_table_as_df(
        "input_alarms", config["db"], "intermediate")

    # Step 4: Filter on-going alarms
    logging.info("Filter on-going alarms")
    df_current_alarms = comp.filter_ongoing_alarms(
        df_all_alarms, df_status, df_alarms_metadata
    )

    # Step 5: Reduce to one alarm per turbine-component
    logging.info("Reduce to one alarm per turbine-component")
    df_current_alarms = df_current_alarms.drop_duplicates(
        subset=['id_wtg_complete','component'], keep='first')

    # Step 6: Complete information
    logging.info("Complete information")
    lst_wtgs = list(df_status['id_wtg_complete'])
    df_full_info = comp.complete_info_per_turbine_component(
        lst_wtgs, lst_components, df_current_alarms
    )

    # Step 7: Read last temperatures
    logging.info("Read last temperatures")
    df_temp_melted = rel.read_last_temperatures(df_temp_signals, config['db'])

    # Step 8: Reduce to one temperature per component
    # We need to see which signal use to represent the component, for the moment
    # we order them alphabetically and use the first one
    logging.info("Reduce to a single component")
    df_temp_final = rel.reduce_to_one_component(df_temp_melted).rename(
        columns={'main_component': 'component'}
    )

    # Step 9: Merge
    logging.info("Merge")
    df_full_info = df_full_info.merge(
        df_temp_final, 
        on=['id_wtg_complete', 'component'],
        how='left'
    )
    df_full_info['code'] = df_full_info['code'].astype('int64')
    df_full_info['overtemperature'] = df_full_info['overtemperature']\
        .fillna(False).astype('int64')

    StatusComponentSchema.validate(df_full_info)
    db.write_df_as_table(
        df_full_info, config['db'], "vis", "status_component",
        index=False, if_exists="replace", chunksize=10000)

    logging.info("--------------------- END SCRIPT ---------------------------")
    logging.info(f"Total time: {datetime.now() - start}")

if __name__ == "__main__":
    main()
