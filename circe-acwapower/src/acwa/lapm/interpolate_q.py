"""
acwa.lapm.interpolate_q

Module to perform interpolation of q1 and q3
"""

from typing import Callable

import pandas as pd
from scipy import interpolate as inter


def interpolate_quantiles(
        df: pd.DataFrame, df_ranges: pd.DataFrame) -> pd.DataFrame:
    
    sectors = set(df_ranges['sector_name'])

    # Obtain interp functions
    dict_interp: dict[str, dict[str, Callable]] = {}
    for sector in sectors:

        df_ranges_aux = df_ranges[df_ranges['sector_name']==sector]
        dict_interp[sector] = {}

        for col in ['q1', 'q3']:

            dict_interp[sector][col] = inter.interp1d(
                df_ranges_aux['wind_speed_bin'], df_ranges_aux[col], bounds_error=False,
            )

    # Apply interp functions
    for sector in sectors:
        for col in ['q1', 'q3']:
            df[f'{col}_interp_{sector}'] = df.apply(
                lambda row: dict_interp[sector][col](row['wind_speed']),
                axis=1
            )

    return df
