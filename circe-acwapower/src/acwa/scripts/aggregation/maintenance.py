"""
acwa.scripts.aggregation.maintenance

Script to count cumulative maintenance hours per turbine
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

import pandas as pd

import acwa.db as db

from acwa.config import read_config
from acwa.data import generate_maintenance_time_limits
from acwa.log import format_basic_logging
from acwa.tables import MaintenanceSchema

def main(year_offset: bool = False):

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("---------------- START SCRIPT: maintenance ------------------")

    logging.info("Read data")
    df_wtg_config = db.read_table_as_df("wtg_config", config['db'], "vis")   
    df_treated_events = db.read_table_as_df('treated_events',config['db'],'vis')

    logging.info("Isolate Maintenance Events")
    # NOTE: Change here the definition of what is considered maintenance
    df_only_maint = df_treated_events[df_treated_events['classification'] == 'Maintenance']
    df_only_maint = df_only_maint.sort_values(by='start_datetime')

    today = datetime.now() 
    if year_offset:
        today = today - relativedelta(year=2023)

    logging.info("Loop over turbines and maintenance years")
    lst_dfs = []
    for i, row in df_wtg_config.iterrows():

        time_limits = generate_maintenance_time_limits(
            row['contractual_date'],
            today = today
        )

        for year in time_limits:

            cond1 = df_only_maint['id_wtg_complete'] == row['id_wtg_complete']
            cond2 = df_only_maint['start_datetime'] >= year['start_date']
            cond3 = df_only_maint['end_datetime'] < year['end_date']

            df_aux = df_only_maint[cond1 & cond2 & cond3].copy()
            df_aux = df_aux[['id_wtg_complete', 'start_datetime', 'end_datetime', 'duration']].reset_index(drop=True)
            df_aux['duration_hours'] = df_aux['duration'] / 3600
            df_aux['cumulative_duration_hours'] = df_aux['duration_hours'].cumsum()

            lst_dfs.append(df_aux)

    df_maint = pd.concat(lst_dfs, axis=0, ignore_index=True)

    logging.info("Writing result")
    df_maint = df_maint[MaintenanceSchema.to_schema().columns.keys()]
    MaintenanceSchema.validate(df_maint)
    db.write_df_as_table(
        df_maint, config['db'], "intermediate", "maintenance",
        index=False, if_exists="replace", chunksize=10000)


if __name__ == "__main__":
    main(year_offset=True)