"""
acwa.scripts.operational.pitch

Script to merge pitch with lambda
"""

import logging

import acwa.data as data
import acwa.db as db
import acwa.oper as oper

from acwa.config import read_config
from acwa.log import format_basic_logging

def main(incremental: bool = True):
    """
    Joins pitch with 10 min data (lambda)

    Args:
        incremental (bool, optional): If True, perform the algorithm only on new
            data (if possible). Defaults to True
    """

    config = read_config()
    format_basic_logging(config['log'])
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True

    logging.info("------------ START SCRIPT: operational.pitch ---------------")

    incremental = data.check_incremental_flag_pitch(incremental, config['db'])
    logging.info(f"Loading {'incremental' if incremental else 'complete'} data")

    logging.info("Read data")
    df_wtg_config = db.read_table_as_df("wtg_config", config["db"], "vis")
    df_pitch = data.read_input_pitch_data(incremental, config["db"])

    logging.info("Calculate lambda")
    df_pitch = oper.calculate_lambda(df_pitch, df_wtg_config)
    df_pitch = df_pitch.drop(columns=['wind_speed', 'rotor_rpm', 'radius'])

    logging.info("Format pitch")
    df_pitch = data.melt_pitch_data(df_pitch)

    logging.info("Write")
    if_exists = "append" if incremental else "replace"
    db.write_df_as_table(
        df_pitch, config['db'], "intermediate", "pitch_with_lambda",
        chunksize=100000, index=False, if_exists=if_exists,
    )

if __name__ == "__main__":
    main(incremental=False)
