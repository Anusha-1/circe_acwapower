"""
acwa.alarms.join.10min.windfarm

Module to join 10min data with alarms at a particular wind farm. 
It uses the wod package
"""

import logging

import pandas as pd

from wod import WindFarm
from wod.alarms.load import load_alarms_from_dataframe

def join_alarms_and_10min_data_in_windfarm(
        df_10min: pd.DataFrame, 
        df_alarms: pd.DataFrame,
        df_wtg_config: pd.DataFrame,
        id_wf: int,
        config: dict) -> pd.DataFrame:
    """
    Join alarms with 10-min data for a wind farm, calculate non-registered 
    alarms and calculate losses

    Args:
        df_10min (pd.DataFrame): 10-min data
        df_alarms (pd.DataFrame): alarms data
        df_wtg_config (pd.DataFrame): WTG data
        id_wf (int): Id of wind farm
        config (dict): Configuration dictionary

    Returns:
        pd.DataFrame: Dataframe with 10-min data and extra columns: alarm, loss,
            producible
    """
    
    logging.info("Create Alarms object")
    dict_alarms = load_alarms_from_dataframe(
        df_alarms,
        turbine_column='id_wtg',
        alarm_column='code',
        start_date_column='start_datetime',
        end_date_column='end_datetime',
        transform_dates_to_datetime=True if config['db']['type'] == 'SQLite' else False
    )

    logging.info("Create Wind Farm object")
    wf = WindFarm(name=id_wf)
    wf.load_dataframe(
        df_10min,
        turbine_column = 'id_wtg',
        datetime_column = 'timestamp',
        speed_column = 'wind_speed',
        power_column = 'power',
        data_validation={
            'drop_consecutive_speed': False,
            'error_threshold': 101 # Over 100% so it doesn't kill processes without valid data
        }
    )

    logging.info("Join alarms for each turbine")
    wf.add_alarms(dict_alarms)
    list_dfs = []
    for turbine in wf.turbines.values():

        # Assigning non registered events
        check = (df_wtg_config['id_wf'] == id_wf) & (df_wtg_config['id_wtg'] == turbine.name)
        min_speed = df_wtg_config[check].iloc[0]['wind_speed_start']
        max_speed = df_wtg_config[check].iloc[0]['wind_speed_stop']
        turbine.add_non_registered_events(
            min_speed = min_speed + 2,
            max_speed = max_speed - 1, 
            mark_boundaries = False,
            label = -1) 
       
        # Formating output
        df_aux = turbine.data[['datetime', 'alarm']].copy()
        df_aux['id_wf'] = id_wf
        df_aux['id_wtg'] = turbine.name
        df_aux = df_aux.rename(
            columns={
                'datetime': 'timestamp',
                'alarm': 'code'})
        
        # Replace the 'Running' label with a code 0
        df_aux['code'] = df_aux['code'].apply(lambda x: 0 if x=='Running' else x)

        list_dfs.append(df_aux)

    logging.info("Merge and return results")
    df_merged = pd.concat(list_dfs)
    return df_10min.merge(df_merged, on=['id_wf','id_wtg','timestamp'])
