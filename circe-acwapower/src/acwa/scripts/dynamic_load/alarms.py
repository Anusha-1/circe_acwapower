"""
acwa.scripts.dynamic_load.alarms

Creates a mockup of real time alarms
"""

from datetime import datetime
import logging

from acwa.mockup import write_dynamic_alarms_table
from acwa.config import read_config
from acwa.db import read_table_as_df

from acwa.log import format_basic_logging

def main(now: datetime | None = None):

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("-------------- START SCRIPT: dynamic_load.alarms -----------")

    logging.info("Load WF Configuration")
    df_wf_config = read_table_as_df("wf_config", config["db"], "vis")

    logging.info("Initializing loop in wind farms")
    for i, row in df_wf_config.iterrows():
        wf_name = row["wf_name"]
        output_table_name = f"realtime_alarms_{wf_name}"

        write_dynamic_alarms_table(
            wf_name, output_table_name, 
            config=config, timezone=row['tz_alarms'], now = now
        )

    logging.info("---------------------- FINISH ------------------------------")

if __name__ == "__main__":
    main()
