"""
acwa.scripts.reference

Calculate reference
"""

import logging

import pandas as pd

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("---------------- START SCRIPT: reference ------------------")

    logging.info("Read data")
    df_wf = read_table_as_df("wf_config", config['db'], "vis")
    df_pitch = read_table_as_df("pitch_with_lambda", config['db'], "intermediate")

    logging.info("Calculating")
    lst_dfs = []
    for i, row in df_wf.iterrows():
        df_aux = df_pitch[df_pitch['id_wtg_complete']==row['reference_turbine']].copy()
        df_aux = df_aux[(df_aux['timestamp']>=row['reference_start']) & (df_aux['timestamp']<=row['reference_end'])]
        lst_dfs.append(df_aux)
    df_ref_pitch = pd.concat(lst_dfs)

    logging.info("Dropping duplicate blades")
    # When we had actual different blades we'll need to check if this makes sense
    df_ref_pitch = df_ref_pitch.drop_duplicates(
        subset=['id_wtg_complete','timestamp', 'statistic', 'pitch_angle']
    )

    logging.info("Merge Wind Farm name")
    df_ref_pitch = df_ref_pitch.merge(
        df_wf[['id_wf', 'wf_name']],
        on = ['id_wf'],
        how='left'
    )

    logging.info("Writing")
    write_df_as_table(
        df_ref_pitch, config['db'], "intermediate", "reference",
        index=False, chunksize=10000, if_exists='replace')
    
    logging.info("End script")

if __name__ == "__main__":
    main()
    