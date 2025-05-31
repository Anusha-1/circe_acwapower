"""
acwa.scripts.status

Script to obtain status table
"""

import logging

import pandas as pd

import acwa.reliability as rel
from acwa.alarms.realtime_status import assign_status
from acwa.alarms.stats import get_turbine_stats

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.db import run_query, write_df_as_table, read_table_as_df
from acwa.tables import StatusSchema

from acwa.tables import Oper10minSchema

def main(year_offset: bool = False):

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("-------------- START SCRIPT: status.turbine ----------------")

    logging.info("Read oper_10min") 
    df_oper_10min = read_table_as_df(
        "oper_10min",
        config['db'],
        "vis"
    ) # We can make this more efficient, not reading all the data. But is not critical

    now = df_oper_10min['timestamp'].max()
    last_24h = now - pd.Timedelta(hours=24)

    # Filter the DataFrame for the last 24 hours
    last_day_df = df_oper_10min[df_oper_10min['timestamp'] >= last_24h]

    last_day_df = last_day_df[Oper10minSchema.to_schema().columns.keys()] 
    last_day_df['angle_deviation_sign'] = last_day_df['angle_deviation_sign'].astype('Int64')  
    Oper10minSchema.validate(last_day_df)

    logging.info("write oper_last_day") 
    write_df_as_table(
        last_day_df,
        config["db"],
        'vis',
        'oper_last_day',
        index=False,
        if_exists="replace",
        chunksize=10000
        )

    ###

    output_table_name = 'status'

    logging.info("Obtain last 10-min")
    df_10min: pd.DataFrame = run_query(
        "select_last_10min_per_turbine",
        config['db'],
        returns="Dataframe"
    )

    logging.info("Obtain last alarms")
    df_alarms: pd.DataFrame = run_query(
        "select_last_alarms_per_turbine",
        config['db'],
        returns="Dataframe"
    )

    logging.info("Filter only ongoing alarms")
    turbines_with_alarms = df_10min[df_10min['code']!=0]['id_wtg_complete']
    df_alarms = df_alarms[df_alarms['id_wtg_complete'].isin(turbines_with_alarms)]
    df_alarms = df_alarms.rename(columns={'code': 'code_alarm'})

    logging.info("Merge info")
    df = df_10min.merge(
        df_alarms[['id_wtg_complete', 'description','priority', 'legacy_type', 'code_alarm']],
        on='id_wtg_complete',
        how='left'
    )

    logging.info("Fill information for OK turbines")
    df['description'] = df['description'].fillna("Turbine OK")
    df['priority'] = df['priority'].fillna(1)
    df['legacy_type'] = df['legacy_type'].fillna("Information")

    logging.info("Assign most updated code")
    df['code'] = df.apply(
        lambda row: row['code'] if pd.isna(row['code_alarm']) else row['code_alarm'],
        axis=1
    )

    logging.info("Assign status")
    df['status'] = df.apply(assign_status, axis=1)
    
    logging.info('obtaining aggregated values')
    query = "aggregate_energy"
    if year_offset:
        query += "_dev"
    df_agg: pd.DataFrame = run_query(
        query,
        config['db'],
        returns="Dataframe"
    )

    logging.info("Joining in status table")
    df = df.merge(df_agg, how='left', on=['id_wf','id_wtg'])

    logging.info("Filling NaN values")
    df['status'] = df['status'].fillna("Running")
    df['code'] = df['code'].fillna(0).astype('Int64')
    df['description'] = df['description'].fillna("Turbine OK") ## Unnecesary here

    logging.info("Calculate MTTR and MTBF")
    df_all_alarms = read_table_as_df("treated_events", config['db'], "vis")
    df_stats = get_turbine_stats(df_all_alarms)
    df = df.merge(df_stats, on='id_wtg_complete')

    logging.info("Adding performance ratios")
    df_perf = read_table_as_df("performance_ratio", config['db'], "vis")
    df_perf_ytd = df_perf[df_perf['period']=='YTD'][['id_wtg_complete', 'PR_manufact']]\
        .rename(columns={"PR_manufact": "pr_ytd"})
    df = df.merge(df_perf_ytd, on="id_wtg_complete", how='left')
    df_perf_mtd = df_perf[df_perf['period']=='MTD'][['id_wtg_complete', 'PR_manufact']]\
        .rename(columns={"PR_manufact": "pr_mtd"})
    df = df.merge(df_perf_mtd, on="id_wtg_complete", how='left')
    df['pr_mtd'] = df['pr_mtd'] * 100
    df['pr_ytd'] = df['pr_ytd'] * 100 #Multiply at origin

    logging.info("Add availabilities")
    df_avail = read_table_as_df("oper_1day", config['db'], "vis")
    df_avail = df_avail[df_avail['day']==df_avail['day'].max()]
    lst_availabilities = df_avail.filter(like='availability').columns.to_list()
    df_avail = df_avail[lst_availabilities + ['id_wtg_complete']]
    df = df.merge(df_avail, on='id_wtg_complete')

    logging.info("Add early alarm system")
    df = rel.apply_early_detection(
        df,
        config['db'])

    df = df[StatusSchema.to_schema().columns.keys()]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
   
    logging.info("Writing table")
    StatusSchema.validate(df)
    write_df_as_table(
        df,
        config['db'],
        'vis',
        output_table_name,
        index=False,
        if_exists="replace"
    )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main(year_offset=True)