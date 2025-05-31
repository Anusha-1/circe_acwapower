"""
acwa.scripts.dynamic_yaw

Script to generate the dynamic yaw changes per hour
"""

import logging

import acwa.db as db
import acwa.yaw as yaw

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.tables import DynamicYawSchema

def main():

    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True
    
    logging.info("Reading data")
    df_1min = db.read_table_as_df(
        'oper_1min',
        config['db'],
        'vis',
        chunksize=10000
    )

    df_wtg_config = db.read_table_as_df("wtg_config", config['db'], "vis")
    df_1min = df_1min.merge(
        df_wtg_config[['id_wtg_complete', 'id_group_complete']]
    )
    
    logging.info("Marking the directional changes")
    df_1min = yaw.mark_all_directional_changes(df_1min)

    logging.info("Counting directional changes")
    df_1min = df_1min.dropna(subset=['wind_direction','nacelle_direction']) # Filter NaN
    df_dyn_yaw = yaw.count_directional_changes(df_1min)

    logging.info("Writing")
    DynamicYawSchema.validate(df_dyn_yaw)
    db.write_df_as_table(
        df_dyn_yaw,
        config['db'],
        'vis',
        'dynamic_yaw',
        if_exists='replace',
        index=False,
        chunksize=10000
    )

if __name__ == "__main__":
    main()
