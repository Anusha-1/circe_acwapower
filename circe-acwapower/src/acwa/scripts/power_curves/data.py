"""
acwa.scripts.power_curves.data

Script to generate power curves through data
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import pytz

import pandas as pd

import acwa.data as data
import acwa.power_curves as pc

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging


def main(
    year_offset: bool = False, 
    lst_data_freq: list[str] = ['10min', '1min'],
    plot: bool = False):
    """
    Generate data-driven Power Curves

    Args:
        year_offset (bool, optional): If True, apply a minus 1 year to allign
            with mockup data. Defaults to False.
        lst_data_freq (list[str], optional): List with data frequencies to
            consider. Defaults to ['10min', '1min'].
        plot (bool, optional): Plot Power Curves. Default to False
    """

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("------------ START SCRIPT: power_curves.data ---------------")

    utc = pytz.timezone('UTC')
    now = datetime.now(tz=utc)  # This will set the temporal horizons
    if year_offset:
        now = now - relativedelta(year=2023)

    for data_freq in lst_data_freq:
        logging.info(f"Calculating Power Curves for {data_freq}")

        df_sectors = read_table_as_df("sectors", config["db"], "vis")
        df_wtg_config = read_table_as_df("wtg_config", config["db"], "vis")
        if data_freq == "10min":
            df_datapoints = read_table_as_df(
                "basic_10min", config["db"], "intermediate")
            df_pc_metadata = read_table_as_df(
                "pc_metadata", config["db"], "vis")            
            df_datapoints_corrected = read_table_as_df(
                "wind_speed_corrections_10min", config["db"], "intermediate")
            output_table_name = "power_curves"
            metadata_table_name = "pc_metadata"
        elif data_freq == "1min":
            df_datapoints = read_table_as_df("oper_1min", config["db"], "vis")
            df_pc_metadata = read_table_as_df(
                "pc_metadata_1min", config["db"], "vis")
            df_datapoints_corrected = read_table_as_df(
                "wind_speed_corrections_1min", config["db"], "intermediate")
            output_table_name = "power_curves_1min"
            metadata_table_name = "pc_metadata_1min"

        logging.info("Merge power with corrected speeds")
        df_datapoints = df_datapoints_corrected.merge(
            df_datapoints[['id_wtg_complete', 'timestamp', 'power', 'code', 'sector_name']], 
            on=['id_wtg_complete', 'timestamp'])
        
        logging.info("Make timestamps timezone-aware")
        df_datapoints['timestamp'] = df_datapoints['timestamp'].dt.tz_localize(
            'UCT', ambiguous='infer')

        logging.info("Preparing time periods for power curve generation")
        min_time = df_datapoints['timestamp'].min()
        time_limits = pc.define_time_limits(now, min_time)
        if data_freq == '1min': # For 1min we are only keeping 'Rolling'
            time_limits = filter(lambda tl: tl['concept'] == 'Rolling', time_limits)

        logging.info("Create power curves")
        lst_df_pc = []
        lst_df_pc_metadata = []
        for dict_limits in time_limits:
            df_pc_aux, df_pc_metadata_aux = pc.generate_power_curves(
                df_datapoints, df_sectors, df_wtg_config, **dict_limits, 
                plot=plot, config_file=config['file_storage'], freq=data_freq
            )
            lst_df_pc.append(df_pc_aux)
            lst_df_pc_metadata.append(df_pc_metadata_aux)

        df_pc = pd.concat(lst_df_pc)
        df_pc_metadata = pd.concat(lst_df_pc_metadata)

        logging.info("Write tables")
        df_pc['power'] = df_pc['power'].fillna(0) # Quick fix for "empty" power curves

        data.write_power_curves(
            df_pc, config["db"], output_table_name=output_table_name)
        data.write_power_curves_metadata(
            df_pc_metadata, config["db"], output_table_name=metadata_table_name)
        
    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main(year_offset=True, plot=True)
