"""
acwa.lapm.wind_speed

Module to obtain LaPM analysis for a given turbine, LaPM mode and wind speed bin
"""

import logging

import pandas as pd
from scipy.stats import kstest

from acwa.lapm.dispersion import calculate_dispersion

def apply_lapm_identification_at_wind_speed(
        df: pd.DataFrame,
        min_points: int = 50) -> pd.DataFrame:
    """
    Apply LaPM identification at a specific turbine, LaPM mode and wind speed.

    Args:
        df (pd.DataFrame): Data points to re-assign based on distributions.
            We should have here data of only two sectors: the main and the LaPM
            sector (note that the main could also be a LaPM)
        min_points (int, optional): Minimum number of data points needed to 
            proceed. If the dataframe has less than this number of points, we
            won't continue with the reassignment (every data point will be
            considered at its sector). Defaults to 50.

    Returns:
        pd.DataFrame: Dataframe with reassigned data points, which means:
        
            - Outliers are filtered out.
            - Points between low q1 and high q1 will be considered as part of
                the low sector
            - Points between low q3 and high q3 will be considered as part of
                the high sector
    """


    ## First, check possible out conditions

    ### 1. Only one sector (this could happen for consecutive non-main sectors)
    if len(set(df['sector_name'])) == 1:
        return df
    
    ### 2. Small number of data points
    if len(df) < min_points:
        return df
    
    ### Add more ??

    lst_sectors = list(set(df["sector_name"]))
    if len(lst_sectors) != 2:
        logging.error("There are no two identified sectors")
        return df

    ## Check distributions
    ks_result = kstest(
        df['power'][df['sector_name']==lst_sectors[0]],
        df['power'][df['sector_name']==lst_sectors[1]],
    )
    p_val = ks_result.pvalue
    if p_val > 0.05:
        return df
    
    ## Detect ranges of the distribution
    df_ranges = calculate_dispersion(df).sort_values(by='median', ascending=False)
    high_sector = df_ranges.iloc[0]['sector_name']
    low_sector = df_ranges.iloc[1]['sector_name']

    ## Re-assign points

    ### Filter out points (we keep in the range between min q1 and max q3)
    df = df[(df['power'] > df_ranges['q1'].min()) & (df['power'] < df_ranges['q3'].max())].copy()

    ### Points between q1 limits are low sector
    # q1_low = df_ranges['q1'][df_ranges['sector_name']==low_sector].iloc[0]
    # q1_high = df_ranges['q1'][df_ranges['sector_name']==high_sector].iloc[0]
    df.loc[(df['power'] > df[f'q1_interp_{low_sector}']) & (df['power'] < df[f'q1_interp_{high_sector}']), 'identified_sector'] = low_sector

    ### Points between q3 limits are high sector 
    # q3_low = df_ranges['q3'][df_ranges['sector_name']==low_sector].iloc[0]
    # q3_high = df_ranges['q3'][df_ranges['sector_name']==high_sector].iloc[0]
    df.loc[(df['power'] > df[f'q3_interp_{low_sector}']) & (df['power'] < df[f'q3_interp_{high_sector}']), 'identified_sector'] = high_sector

    return df
