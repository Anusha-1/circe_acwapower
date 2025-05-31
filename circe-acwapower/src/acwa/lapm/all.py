"""
acwa.lapm.all

Apply LaPM identification analysis over all the turbines
"""

import pandas as pd

from acwa.lapm.sectors import apply_lapm_identification_at_all_sectors

def apply_lapm_identification_at_all_turbines(
        df_data: pd.DataFrame, 
        df_sectors: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the LaPM identification method to every turbine in a loop

    Args:
        df_data (pd.DataFrame): Dataframe with datapoints 10-min or 1-min
        df_sectors (pd.DataFrame): Sector information

    Returns:
        pd.DataFrame: Dataframe with reassigned id as a result
    """

    ## We begin by identifying each data point with the mode it belongs to by
    ## the direction. Only if we find "hard evidence" against a point, we will
    ## overturn this decision 
    df_data['identified_sector'] = df_data['sector_name']


    turbines = list(set(df_sectors['id_wtg_complete']))
    turbines.sort()

    lst_dfs = []
    for turb in turbines:

        df_aux = df_data[df_data['id_wtg_complete']==turb].copy()
        df_sectors_aux = df_sectors[df_sectors['id_wtg_complete']==turb].copy()

        df_result = apply_lapm_identification_at_all_sectors(
            df_aux, df_sectors_aux)

        if df_result is not None:
            lst_dfs.append(df_result)

    return pd.concat(lst_dfs)
