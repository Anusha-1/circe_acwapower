"""
acwa.scripts.allocation

Script to allocate duration and loss per day and different categories 
(alarm code, component and manufacturer concept)
"""

import logging

import acwa.data as data
import acwa.losses as loss

from acwa.config import read_config
from acwa.db import read_table_as_df
from acwa.log import format_basic_logging

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("---------------- START SCRIPT: allocation ------------------")
    
    logging.info("Read oper_10min") 
    df_oper_10min = read_table_as_df(
        "oper_10min",
        config['db'],
        "vis"
    )

    logging.info("Read treated alarms")
    df_alarms = read_table_as_df(
        "treated_events",
        config['db'],
        "vis"
    )
    logging.info(f"Number of events: {len(df_alarms)}")

    logging.info("Extend by days")
    cols_to_keep = [
        'id_wf',
        'id_wtg',
        'id_wtg_complete',
        'code',
        'component',
        'manufacturer_availability',
        'start_datetime',
        'end_datetime',
        'duration'
    ]
    df_alarms_ext = data.extend_by_days(df_alarms[cols_to_keep])
    df_alarms_ext['day'] = df_alarms_ext["start_datetime"].apply(lambda x: x.date())

    logging.info("Remove underperforming alarms and missing data")
    df_alarms_ext = df_alarms_ext[df_alarms_ext['code']!=-2]
    df_alarms_ext = df_alarms_ext[df_alarms_ext['code']!=-3]

    logging.info("Distribute losses in alarms")
    df_alarms_ext = loss.distribute_losses_in_alarms(
        df_alarms_ext, df_oper_10min, 
        non_registered_alarms=False,
        codes_to_ignore=[-2, -3]) 
    # Ignore -2 (under-performing) as it is not unavailable, they have no losses.
    # Also, we have remove them from the alarms. 
    # Also ignoring -3   
    
    logging.info("Group by alarm")
    df_group = df_alarms_ext.groupby(
        ['id_wf','id_wtg','id_wtg_complete','day', 'code', 'component']).agg(
            {'duration': 'sum',
             'losses': 'sum'}
        ).reset_index()
    
    logging.info("Writing treated_events_1_day")
    data.write_treated_events_1day(df_group, config['db'])    

    logging.info("Group by component")
    df_group = df_alarms_ext.groupby(
        ['id_wf','id_wtg','id_wtg_complete','day', 'component']).agg(
            {'duration': 'sum',
             'losses': 'sum'}
        ).reset_index()
    
    logging.info("Writing component_availabilities_1day")
    data.write_component_availabilities_1day(df_group, config['db'])  

    logging.info("Group by manufacturer")
    df_group = df_alarms_ext.groupby(
        ['id_wf','id_wtg','id_wtg_complete','day', 'manufacturer_availability']).agg(
            {'duration': 'sum',
             'losses': 'sum'}
        ).reset_index()
    
    logging.info("Writing manufacturer_availabilities_1day")
    data.write_manufacturer_availabilities_1day(df_group, config['db'])  

    logging.info("----------------------- FINISH -----------------------------")


if __name__ == "__main__":
    main()