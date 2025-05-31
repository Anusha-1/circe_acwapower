"""
acwa.losses.calculate_windfarm

Calculate losses at a wind farm
"""

import logging

import pandas as pd

from wod import WindFarm
from wod.alarms.load import load_alarms_from_dataframe

from acwa.power_curves import assign_default_power_curve

def calculate_losses_in_windfarm(
        df_10min: pd.DataFrame, 
        df_alarms: pd.DataFrame,
        df_wtg_config: pd.DataFrame,
        id_wf: int,
        df_pc_metadata: pd.DataFrame,
        config: dict) -> pd.DataFrame:
    """
    Join alarms with 10-min data for a wind farm, calculate non-registered 
    alarms and calculate losses

    Args:
        df_10min (pd.DataFrame): 10-min data
        df_alarms (pd.DataFrame): alarms data
        df_wtg_config (pd.DataFrame): WTG data
        id_wf (int): Id of wind farm
        df_pc_metadata (pd.DataFrame): Dataframe with power curve metadata
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
        }
    )

    logging.info("Join alarms for each turbine")
    wf.add_alarms(dict_alarms)
    list_dfs = []
    for turbine in wf.turbines.values():

        # Assigning non registered events
        check = (df_wtg_config['id_wf'] == id_wf) & (df_wtg_config['id_wtg'] == turbine.name)
        min_speed = df_wtg_config[check].iloc[0]['wind_speed_start']
        turbine.add_non_registered_events(min_speed = min_speed + 0.5) 

        # Assigning a power curve
        pc = assign_default_power_curve(df_pc_metadata, f"{id_wf}-{turbine.name}", config)
        turbine.add_power_curves(pc)

        # Calculating losses
        turbine.get_losses()

        # Formating output
        df_aux = turbine.data[['datetime', 'alarm', 'power_reference', 'loss']].copy()
        df_aux['id_wf'] = id_wf
        df_aux['id_wtg'] = turbine.name
        df_aux = df_aux.rename(
            columns={
                'datetime': 'timestamp',
                'power_reference': 'producible_power'})
        list_dfs.append(df_aux)

    logging.info("Merge and return results")
    df_merged = pd.concat(list_dfs)
    return df_10min.merge(df_merged, on=['id_wf','id_wtg','timestamp'])
