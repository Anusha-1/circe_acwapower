"""
acwa.mockup.dynamic_alarms_table

Module with function to create a dynamic raw  alarms stable by using the data 
from the static raw table
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import pytz

import pandas as pd

from acwa.db import (
    run_query,
    write_df_as_table
)
from acwa.mockup import correct_alarm_times

def write_dynamic_alarms_table(
    wf_name: str,
    output_table_name: str,
    config: dict | None = None,
    timezone: str = 'UTC',
    now: datetime | None = None,
) -> None:
    """
    Creates/Updates the realtime alarms table for a given wind farm

    Args:
        wf_name (str): Name of the wind farm
        output_table_name (str): Name of the output table
        config (dict | None, optional): Configuration options. Defaults to None.
        timezone (str, optional): Timezone of the alarms data. Defaults to 'UTC'.
        now (datetime | None, optional): Temporal limit to consider. 
            If None, obtain present moment from system. Defaults to None
    """
    
    logging.info("Obtaining times")
    tz = pytz.timezone(timezone)
    now = now if now is not None else datetime.now()
    end_time = now.astimezone(tz) - relativedelta(year=2023)


    logging.info(f"Read alarms for {output_table_name}")
    df: pd.DataFrame = run_query(
        f"read_alarms_{wf_name}",
        config["db"],
        params={"end": end_time.strftime("%Y-%m-%d %H:%M:%S")},
        returns="Dataframe",
    )

    df = correct_alarm_times(df, 2023, end_time, tz)

    logging.info("Writing table")
    write_df_as_table(
        df,
        config["db"],
        "raw",
        output_table_name,
        index=False,
        if_exists="replace",
    )
