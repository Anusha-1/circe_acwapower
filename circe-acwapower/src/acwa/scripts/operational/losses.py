"""
acwa.scripts.operational.losses.py

Script with part 2 of the "operational" algorithm to update the "real time"
operational tables: oper_10min and treated_events
"""

import logging

import pandas as pd

import acwa.alarms as alarms
import acwa.data as data
import acwa.losses as loss
import acwa.oper as oper

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging


def main(incremental: bool = True):
    """
    Calculate different operational KPIs for 10 min data and alams

    Args:
        incremental (bool, optional): If True, perform the algorithm only on new
            data (if possible). Defaults to True
    """

    config = read_config()
    format_basic_logging(config["log"])
    logging.getLogger("sqlalchemy.engine.Engine").disabled = True

    logging.info("------------ START SCRIPT: operational.losses --------------")

    # Check incremental flag. We decide here if we will load the data
    # incrementally, or completely
    incremental = data.check_incremental_flag(incremental, config["db"])
    logging.info(f"Loading {'incremental' if incremental else 'complete'} data")

    logging.info("Read sector")
    df_sectors = read_table_as_df("sectors", config["db"], "vis")

    logging.info("Read 10-min basic data")
    df_10min = data.read_basic_10min_data(incremental, config["db"])

    logging.info("Read alarms")
    df_alarms = data.read_basic_alarms(incremental, config["db"])

    logging.info("Introduce historical producible")
    df_10min = loss.obtain_producible(df_10min, df_sectors, config["db"])

    logging.info("Calculate losses")
    df_10min["loss"] = df_10min.apply(
        lambda row: None
        if (row["power"] is None or row["producible"] is None)
        else max(row["producible"] - row["power"], 0)
        if row["code"] != 0
        else 0,
        axis=1,
    ).astype(float)

    logging.info("Calculate efficiency ratio")
    df_10min = oper.calculate_production_ratio(df_10min)

    logging.info("Calculate energy availability")
    df_10min = oper.calculate_energy_availability(df_10min)

    logging.info("Adding missing data alarms")
    df_alarms = alarms.extract_all_custom_alarms(
        df_10min, df_alarms, "Missing data")

    logging.info("Distribute the losses in the alarms")
    df_alarms = loss.distribute_losses_in_alarms(df_alarms, df_10min)

    logging.info("Calculating performance losses")
    df_10min = loss.calculate_performance_losses(df_10min, config["db"])
    
    logging.info("Adding underperforming alarms")
    df_alarms = alarms.extract_all_custom_alarms(
        df_10min, df_alarms, "Underperforming")
    
    logging.info("Re-evaluate priority in alarms")
    # This fixes overlapping during communication loss.
    # Maybe we could re-schedule these processes in a more efficient way...
    df_alarms = alarms.avoid_overlapping_alarms(df_alarms)

    if len(df_alarms) > 0:
        logging.info("Writing alarms with losses")
        data.write_alarms_with_losses(df_alarms, incremental, config["db"])

    df_10min["validation_status"] = df_10min.apply(
        lambda row: not any(pd.isna(row)), axis=1
    )

    logging.info("Writing oper_10min")
    data.write_oper_10min(df_10min, incremental, config["db"])

    logging.info("----------------------- FINISH -----------------------------")


if __name__ == "__main__":
    main(incremental=False)
