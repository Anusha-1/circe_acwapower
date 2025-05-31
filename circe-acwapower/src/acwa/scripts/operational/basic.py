"""
acwa.scripts.operational_basic

Script with part 1 of the "operational" algorithm to update the "real time"
operational tables: basic_10min and basic_alarms
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import pytz

import acwa.alarms as alarms
import acwa.data as data
import acwa.oper as oper
import acwa.yaw as yaw

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging


def main(incremental: bool = True, year_offset: bool = False):
    """
    Joins 10min and alarm data

    Args:
        incremental (bool, optional): If True, perform the algorithm only on new
            data (if possible). Defaults to True
        year_offset (bool, optional):  If True, put the present moment in 2023
            when retrieving data (True to work with mockup data in 2023, in
            production should work with False). Defaults to False
    """

    config = read_config()
    format_basic_logging(config["log"])
    logging.getLogger("sqlalchemy.engine.Engine").disabled = True

    logging.info("------------ START SCRIPT: operational.basic ---------------")

    # Check incremental flag. We decide here if we will load the data
    # incrementally, or completely
    incremental = data.check_incremental_flag_basic(incremental, config["db"])
    logging.info(f"Loading {'incremental' if incremental else 'complete'} data")

    # Loading metadata
    now = datetime.now(tz=pytz.timezone("UTC"))
    now = now - year_offset * relativedelta(year=2023)
    now = now.replace(tzinfo=None)

    logging.info("Read wtg config")
    df_wtg_config = read_table_as_df("wtg_config", config["db"], "vis")

    logging.info("Obtain priority alarms")
    df_alarms = alarms.obtain_priority_alarms(now, config["db"], incremental)

    logging.info("Read 10-min input data")
    df_10min = data.read_input_10min_data(incremental, config["db"])
    df_10min = data.aggregate_values_from_1min(
        df_10min, "temperature", config["db"], incremental=incremental
    )

    if len(df_10min) == 0:
        logging.warning("No data")
        return

    logging.info("Joining 10min with alarms")
    df_10min = alarms.join_alarms_and_10min_data(
        df_10min, df_alarms, df_wtg_config, config
    )

    logging.info("Detect communitation losses")
    df_10min = data.fill_gaps(df_10min, "10min")

    logging.info("reading met mast data 10min")
    df_met_mast = read_table_as_df("oper_met_mast", config["db"], "vis")
    met_mast_config = read_table_as_df("met_mast_metadata", config["db"], "vis")

    logging.info("Calculate air density 10-min ")
    df_10min = data.calculate_density_10min(
        df_10min,
        df_wtg_config,
        df_met_mast,
        met_mast_config,
        incremental=incremental,
    )

    logging.info("Calculate cp")
    df_10min = oper.calculate_cp_10min(df_10min, df_wtg_config)

    logging.info("Calculate lambda")
    df_10min = oper.calculate_lambda(df_10min, df_wtg_config)

    logging.info("Calculate wind speed correction")
    df_densities = read_table_as_df("densities", config["db"], "vis")
    df_densities = df_densities[df_densities["main"] == 1]
    df_10min = df_10min.merge(
        df_densities[["id_wf", "density"]].rename(
            columns={"density": "reference_density"}
        ),
        on="id_wf",
        how="left",
    )
    df_10min = data.correct_speed_with_density(df_10min)

    logging.info("Correct to all densities")
    df_10min_corrected = data.correct_by_densities(df_10min, config["db"])

    logging.info("Clasify lambda and windspeed in bins")
    if incremental:
        df_reference = read_table_as_df(
            "basic_10min",  ##aqui habra algo que arreglar creo yo porque basic_10min has no temps corrected
            config["db"],
            "intermediate",
        )
    else:
        df_reference = df_10min
    df_10min = data.classify_in_bin(
        df_10min,
        ["wind_speed_corrected", "lambda_parameter"],
        0.1,
        df_reference=df_reference,
    )

    logging.info("Calculate sector")
    df_sectors = read_table_as_df("sectors", config["db"], "vis")
    df_10min = data.assign_sector_10min(df_10min, df_sectors)

    logging.info("Yaw static calculations")
    df_10min = yaw.calculate_yaw_static_variables(df_10min)
    
    logging.info("Write basic 10 min data")
    data.write_basic_10min(df_10min, incremental, config["db"])

    logging.info("Write basic priority alarms")
    data.write_priority_alarms(df_alarms, incremental, config["db"])

    logging.info("Write wind speed corrections")
    data.write_wind_speed_corrections(
        df_10min_corrected, incremental, config["db"]
    )

    logging.info("----------------------- FINISH -----------------------------")


if __name__ == "__main__":
    main(incremental=False, year_offset=True)
