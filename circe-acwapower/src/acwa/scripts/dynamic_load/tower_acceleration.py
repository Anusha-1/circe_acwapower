"""
acwa.scripts.dynamic_load.pitch

Module to write real-time dynamic pitch
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import pytz

import pandas as pd

import acwa.data as data

from acwa.config import read_config
from acwa.db import (
    check_table,
    run_query,
    write_df_as_table,
    read_table_as_df,
)
from acwa.log import format_basic_logging


def main(now: datetime | None = None):
    ### NOTE: Consider divide this logic into functions...

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("-------------- START SCRIPT: dynamic_load.tower_acceleration ------------")

    logging.info("Load WF Configuration")
    df_wf_config = read_table_as_df("wf_config", config["db"], "vis")

    logging.info("Initializing loop in wind farms")
    for i, row in df_wf_config.iterrows():
        wf_name = row["wf_name"]

        logging.info("Obtaining times")
        tz = pytz.timezone(row["tz_alarms"])
        now = now if now is not None else datetime.now()
        end_time = now.astimezone(tz) - relativedelta(year=2023)

        output_table_name = f"realtime_tower_acceleration_{wf_name}"
        logging.info(f"Checking if table {output_table_name} exists")
        check = check_table(output_table_name, config["db"], "raw")

        if check:
            logging.info(f"Table {output_table_name} already exists")

            logging.info("Extracting last datetimes")
            df_last_times: pd.DataFrame = run_query(
                f"max_time_tower_acceleration_{wf_name}", config["db"], returns="Dataframe"
            )
            if config["db"]["type"] == "SQLite":
                max_time = (
                    datetime.strptime(
                        df_last_times["max_time"].iloc[0], "%Y-%m-%d %H:%M:%S.%f"
                    )
                    + timedelta(seconds=1)
                )
            elif config["db"]["type"] == "Azure":
                max_time = (
                    df_last_times["max_time"].iloc[0].to_pydatetime()
                    + timedelta(seconds=1) ## Add this to prevent bug
                )

            logging.info("Retrieving new data")
            df = run_query(
                f"read_new_tower_acceleration_{wf_name}",
                config["db"],
                params={
                    "end": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "max": max_time.strftime("%Y-%m-%d %H:%M:%S"),
                },
                returns="Dataframe",
            )

            if len(df) > 0:

                ## Correct times
                df = data.transform_to_datetime(
                    df,
                    "PCTimeStamp",
                    "%Y-%m-%d %H:%M:%S.%f",
                    dest_col="PCTimeStamp",
                    drop_original_col=False,
                )

                logging.info("Writing table")
                write_df_as_table(
                    df,
                    config["db"],
                    "raw",
                    output_table_name,
                    index=False,
                    if_exists="append",
                )

        else:
            logging.info(f"Table {output_table_name} does not exist")

            df: pd.DataFrame = run_query(
                f"read_tower_acceleration_{wf_name}",
                config["db"],
                params={"end": end_time.strftime("%Y-%m-%d %H:%M:%S")},
                returns="Dataframe",
            )

            ## Correct times
            df = data.transform_to_datetime(
                df,
                "PCTimeStamp",
                "%Y-%m-%d %H:%M:%S.%f",
                dest_col="PCTimeStamp",
                drop_original_col=False,
            )

            logging.info("Writing table")
            write_df_as_table(
                df,
                config["db"],
                "raw",
                output_table_name,
                index=False,
                if_exists="replace",
            )

    logging.info("---------------------- FINISH ------------------------------")


if __name__ == "__main__":
    main()
