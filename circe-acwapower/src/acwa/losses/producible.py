"""
acwa.losses.producible

Obtain producible from historical power curves
"""

import logging

import pandas as pd
import numpy as np
from scipy import interpolate

from acwa.db import read_table_as_df, check_table
from acwa.scripts.power_curves.data import main as obtain_power_curves # Avoid circular import

def obtain_producible(
        df_10min: pd.DataFrame,
        df_sectors: pd.DataFrame,
        config_db: dict) -> pd.DataFrame:
    """
    Obtain producible, interpolating from historical power curve 

    Args:
        df_10min (pd.DataFrame): 10min data
        df_sectors (pd.DataFrame): Sectors
        config_db (dict): Database config

    Returns:
        pd.DataFrame: 10min data with extra column 'producible'
    """

    if not check_table("power_curves", config_db, "vis"):
        obtain_power_curves()

    # Read power curves and power curves metadata
    df_pc = read_table_as_df(
        "power_curves",
        config_db,
        "vis"
    )
    df_pc_metadata = read_table_as_df(
        "pc_metadata",
        config_db,
        "vis"
    )
    df_pc = df_pc.merge(df_pc_metadata, on='pc_id')
    df_pc = df_pc[(df_pc['concept']=='Historical') & (df_pc['period']=='12 months')]

    # Filter by main density
    df_wtg_config = read_table_as_df("wtg_config", config_db, "vis")
    df_dens = read_table_as_df("densities", config_db, "vis")
    df_pc = df_pc.merge(
        df_wtg_config[['id_wtg_complete', 'id_wf']],
        on='id_wtg_complete',
        how='left'
    )
    df_dens['density'] = df_dens['density'].astype(str)
    df_pc = df_pc.merge(
        df_dens.rename(columns={'main': 'main_density'}),
        on=['id_wf', 'density'],
        how='left'
    )
    df_pc = df_pc[df_pc['main_density']==1]

    df_10min['producible'] = np.nan # Default value

    # Loop in rows in sectors dataframe (i.e. combinations of turbine and sector)
    for i, row in df_sectors.iterrows():

        # Indices of turbine-sector
        indices = (df_10min['id_wtg_complete']==row['id_wtg_complete']) & (df_10min['sector_name']==row['sector_name'])

        # Isolate Power Curve
        df_pc_aux = df_pc[(df_pc['id_wtg_complete']==row['id_wtg_complete']) & (df_pc['sector_name']==row['sector_name'])].copy()

        if len(df_pc_aux) == 0:

            logging.warning(f"Missing curve(s) for {row['id_wtg_complete']} | {row['sector_name']}. We stop here to calculate them")

            obtain_power_curves() # If a curve is missing, it runs the process to obtain all power curves. 
                                  # This should be only necessary once at most...
            # Read power curves and power curves metadata
            df_pc = read_table_as_df(
                "power_curves",
                config_db,
                "vis"
            )
            df_pc_metadata = read_table_as_df(
                "pc_metadata",
                config_db,
                "vis"
            )
            df_pc = df_pc.merge(df_pc_metadata, on='pc_id')
            df_pc = df_pc[(df_pc['concept']=='Historical') & (df_pc['period']=='12 months')]  
            df_pc_aux = df_pc[(df_pc['id_wtg_complete']==row['id_wtg_complete']) & (df_pc['sector_name']==row['sector_name'])].copy()          

        # Interpolating function
        f = interpolate.PchipInterpolator(df_pc_aux['bin'], df_pc_aux['power'])

        # Assign producible
        df_10min.loc[indices, 'producible'] = f(df_10min.loc[indices, "wind_speed_corrected"])

    return df_10min
