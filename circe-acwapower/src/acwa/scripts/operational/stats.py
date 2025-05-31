"""
acwa.scripts.operational_stats.py

Script with part 3 of the "operational" algorithm to update the "real time" 
operational tables: oper_10min and treated_events
"""

import logging

import acwa.alarms as alarms

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging
from acwa.tables import TreatedEventsSchema

def main():

    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------ START SCRIPT: operational_stats ---------------")

    logging.info("Read alarms")
    df_alarms = read_table_as_df(
        'alarms_with_losses', config['db'], 'intermediate')

    logging.info("Calculate stats")
    df_alarms = alarms.calculate_alarm_stats(df_alarms)

    logging.info("Write")
    TreatedEventsSchema.validate(df_alarms)
    df_alarms = df_alarms[TreatedEventsSchema.to_schema().columns.keys()]
    write_df_as_table(
        df_alarms,
        config['db'],
        'vis',
        'treated_events',
        if_exists='replace',
        index=False
    )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()