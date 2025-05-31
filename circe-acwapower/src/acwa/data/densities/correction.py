"""
acwa.data.densities.correction

Correct by densities
"""

import pandas as pd

from acwa.db import read_table_as_df
from acwa.data.calc import correct_speed_with_density, correct_speed_with_density_auto

def correct_by_densities(
        df_10min: pd.DataFrame,
        config_db: dict) -> pd.DataFrame:
    """
    Correct wind speed at different densities

    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe where each data point has been corrected to
            different densities (as different rows)
    """

    df_densities = read_table_as_df("densities", config_db, "vis")

    # Loop in wind farms
    lst_wfs = list(set(df_densities['id_wf']))
    lst_columns_to_keep = ['id_wtg_complete', 'timestamp', 'wind_speed', 'density']
    lst_dfs = []
    for id_wf in lst_wfs:

        df_aux = df_10min[df_10min['id_wf']==id_wf][lst_columns_to_keep].copy()
        df_dens_aux = df_densities[df_densities['id_wf']==id_wf]
        lst_densities = list(df_dens_aux['density'])

        for density in lst_densities:
            df_aux_corrected = correct_speed_with_density(
                df_aux, density).copy()
            df_aux_corrected['density_corrected'] = str(density) 

            lst_dfs.append(df_aux_corrected)

        ## Auto correction (only if there are mote than one density)
        if len(lst_densities) > 1:
            df_aux_corrected = correct_speed_with_density_auto(
                df_aux, lst_densities).copy()
            df_aux_corrected['density_corrected'] = 'auto' 
            lst_dfs.append(df_aux_corrected)

    return pd.concat(lst_dfs, ignore_index=True)
