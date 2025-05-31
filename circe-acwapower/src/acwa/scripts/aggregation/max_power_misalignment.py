"""
acwa.scripts.max_power_misallignment

Script to compute the misallignment that produces maximum power
"""

import logging

import acwa.db as db
import acwa.yaw as yaw

from acwa.config import read_config
from acwa.log import format_basic_logging

def main(year_offset: bool = False):

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("Max Power Misallignment for 10min data")
    df_datapoints = db.read_table_as_df("oper_10min", config['db'], "vis")
    df_datapoints['timestamp'] = df_datapoints['timestamp'].dt.tz_localize(
            'UCT', ambiguous='infer')
    yaw.fit_all_time_limits_max_power_misallignments(
        df_datapoints, config['db'], "10min", year_offset = year_offset
    )

    logging.info("Max Power Misallignment for 1min data")
    df_datapoints = db.read_table_as_df("oper_1min", config['db'], "vis")
    df_datapoints['timestamp'] = df_datapoints['timestamp'].dt.tz_localize(
            'UCT', ambiguous='infer')
    yaw.fit_all_time_limits_max_power_misallignments(
        df_datapoints, config['db'], "1min", year_offset = year_offset
    )


if __name__ == "__main__":
    main(year_offset=True)