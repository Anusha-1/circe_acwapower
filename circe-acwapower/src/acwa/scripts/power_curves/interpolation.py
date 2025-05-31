"""
acwa.scripts.power_curves_interpolation

Script to interpolate power curves.

NOTE: Ad-hoc process due to Power BI limitations
"""

import logging

import acwa.data as data
import acwa.power_curves as pc

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main():

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("-------- START SCRIPT: power_curves.interpolation ----------")

    for data_type in ["10min", "1min"]:

        logging.info(f"Calculating interpolated Power Curves for {data_type}")

        logging.info("Read tables")
        if data_type == '10min':
            df_pc = read_table_as_df("power_curves", config['db'], "vis", 
                                    chunksize=10000)
            df_pc_metadata = read_table_as_df("pc_metadata", config['db'], "vis")
            output_table_name = "interpolated_power_curves"
        elif data_type == '1min':
            df_pc = read_table_as_df("power_curves_1min", config['db'], "vis", 
                                    chunksize=10000)
            df_pc_metadata = read_table_as_df("pc_metadata_1min", config['db'], "vis")
            output_table_name = "interpolated_power_curves_1min"
        
        logging.info("Interpolating Power Curves")
        df_interpolated = pc.interpolate_power_curves(df_pc, df_pc_metadata)

        logging.info("Merging metadata information")
        df_wtg_config = read_table_as_df(
            "wtg_config", config['db'], "vis"
        )
        df_interpolated = df_interpolated.merge(
            df_wtg_config[['id_wtg_complete', 'wf_name', 'wtg_name', 'id_group_complete','group']],
            on='id_wtg_complete',
            how='left'
        )

        logging.info("Writing interpolated power curves")
        data.write_interpolated_power_curves(
            df_interpolated, config["db"], output_table_name=output_table_name)

if __name__ == "__main__":
    main()
