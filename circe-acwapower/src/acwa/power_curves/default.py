"""
acwa.power_curves.default

Module to assign a default power curve for each turbine
"""

import logging

import pandas as pd

from wod.power_curve import PowerCurve

from acwa.db import run_query

def assign_default_power_curve(
        df_pc_metadata: pd.DataFrame,
        id_wtg_complete: str,
        config: dict) -> PowerCurve:
    """
    Function to return a "default" power curve for each turbine. It searches for
    the Power Curve with the largest sector and highest density

    Args:
        df_pc_metadata (pd.DataFrame): Dataframe with power curve metadata
        id_wtg_complete (str): Id of WTG 
        config (dict): Configuration dictionary

    Returns:
        PowerCurve: PowerCurve object
    """

    logging.info(f"Assigning default power curve to {id_wtg_complete}")

    # Extracting a pc_id
    df_aux = df_pc_metadata[df_pc_metadata['id_wtg_complete']==id_wtg_complete].copy() #Consider changing this to id_wtg_complete    
    def __calculate_sector_size(row):
        diff = row['sector_fin'] - row['sector_ini']
        if diff > 0:
            return diff      
        return (360 - row['sector_ini']) + row['sector_fin']
    df_aux['sector_size'] = df_aux.apply(__calculate_sector_size, axis=1)
    df_aux = df_aux[df_aux['sector_size'] == df_aux['sector_size'].max()]
    df_aux = df_aux[df_aux['density'] == df_aux['density'].min()]
    pc_id = df_aux.iloc[0]['pc_id']
    logging.info(f"Exctracted pc_id: {pc_id}. Retrieving power curve")

    # Reading and formatting power curve
    df_pc: pd.DataFrame = run_query(
        "select_power_curve",
        config['db'],
        returns="Dataframe",
        params={"power_curve_id": pc_id})    
    df_pc = df_pc[['bin','power','sigma']]
    df_pc = df_pc.rename(columns={'sigma': 'deviation'})

    # Building and returning PowerCurve object
    pc = PowerCurve.from_dataframe(df_pc)
    return pc
