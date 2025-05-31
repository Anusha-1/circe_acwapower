"""
acwa.lapm.sectors

Module to apply LaPM identification to all possible LaPM modes for a turbine
"""

import pandas as pd
from scipy import interpolate

from acwa.lapm.closest_sector import obtain_closest_sector
from acwa.lapm.wind_speed import apply_lapm_identification_at_wind_speed
from acwa.lapm.dispersion import calculate_dispersion
from acwa.lapm.interpolate_q import interpolate_quantiles

def apply_lapm_identification_at_all_sectors(
        df: pd.DataFrame, df_sectors: pd.DataFrame, 
) -> pd.DataFrame | None:
    """
    Apply LaPM identification inside the data of a turbine, to all its possible
    sectors

    Args:
        df (pd.DataFrame): Dataframe of points
        df_sectors (pd.DataFrame): Sector information

    Returns:
        pd.DataFrame | None: Dataframe with result column: 'identified_sector'.
            Returns None if there are no LaPM modes.
    """
    
    list_of_sectors = list(set(df_sectors['sector_name']))
    number_of_sectors = len(list_of_sectors)

    if number_of_sectors == 1:
        return None
    
    df_lapm_sectors = df_sectors[~df_sectors['main']]
    lst_lapm_sectors = list(set(df_lapm_sectors['sector_name']))
    if len(lst_lapm_sectors) == 1:
        df['closest_sector'] = lst_lapm_sectors[0]
    else:
        series_sector = df.apply(
            obtain_closest_sector, 
            axis=1, 
            args=(df_lapm_sectors,))
    
        df['closest_sector'] = series_sector

    ## Loop at each not main sector
    lst_df = []
    for lapm_sector in lst_lapm_sectors:

        ## Isolate the points in the area of influence of the LaPM mode.
        df_aux = df[df['closest_sector']==lapm_sector].copy()

        ## Loop in wind speeds
        lst_ws_bins = list(set(df['wind_speed_bin']))
        lst_ws_bins.sort()

        ## Calculate dispersion stats
        df_ranges = calculate_dispersion(df_aux)
        df_aux = interpolate_quantiles(df_aux, df_ranges)
        
        for ws in lst_ws_bins:

            df_aux_ws = df_aux[df_aux['wind_speed_bin']==ws]
            lst_df.append(
                apply_lapm_identification_at_wind_speed(df_aux_ws)
            )


    return pd.concat(lst_df)
