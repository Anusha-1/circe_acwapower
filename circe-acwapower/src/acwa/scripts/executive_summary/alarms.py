"""
acwa.scripts.executive_summary.alarms

Script to identify alarms for executive summary
"""

import logging

import acwa.data as data

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging
from acwa.tables import ExecutiveSummaryAlarms

def main():
    
    config = read_config()
    format_basic_logging(config["log"])
    logging.info("--------- START SCRIPT: executive_summary.alarms -----------")

    logging.info("Read data")
    df_treated_events_1day = read_table_as_df(
        "treated_events_1day", config["db"], "vis")

    logging.info("Summarize alarms")
    df_alerts = data.extract_summary_alarms(df_treated_events_1day)
    df_alerts['id_wf_period'] = df_alerts['id_wf'] + '-' + df_alerts['year'] + '-' + df_alerts['month'] 

    logging.info("Writing")
    df_alerts = df_alerts[ExecutiveSummaryAlarms.to_schema().columns.keys()]
    ExecutiveSummaryAlarms.validate(df_alerts)
    write_df_as_table(
        df_alerts,
        config["db"],
        "vis",
        "executive_summary_alarms",
        index=False,
        if_exists="replace",
    )

    logging.info("End script")

if __name__ == "__main__":
    main()
