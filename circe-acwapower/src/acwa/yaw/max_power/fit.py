"""
acwa.yaw.max_power.fit

Module to obtain misallignment that produces maximum power
"""

from datetime import datetime
import logging

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def poly2(x, a, b, c):
    return a * x * x + b * x + c

def obtain_max_power_misallignment(
    df: pd.DataFrame,
    start: datetime | None = None,
    end: datetime | None = None,
    period: str = 'All',
    min_speed: float = 4.0,
    max_speed: float = 15.0,
    max_abs_angle_deviation: float = 9.0,
    min_number_points: int = 2,
) -> pd.DataFrame:
    
    # Filter only necessary columns for simplicity
    lst_columns_to_keep = [
        "id_wtg_complete",
        "timestamp",
        "wind_speed",
        "power",
        "angle_deviation",
        "code",
    ]
    for col in lst_columns_to_keep:
        assert col in df.columns, f"Missing column {col}"
    df = df[lst_columns_to_keep].copy()

    # Filter times
    if start is not None:
        df = df[df['timestamp'] >= start]
    if end is not None:
        df = df[df['timestamp'] <= end]

    # Bin wind and angle deviation
    df["wind_speed_bin"] = df["wind_speed"].round(0)
    df["angle_deviation_bin"] = df["angle_deviation"].round(0)

    # Filters
    ## code = 0 (only OK)
    ## speed >= min_speed m/s and speed <= max_speed m/s
    ## angle deviation in [-X,X] (X = max_abs_angle_deviation)
    df = df[
        (df["code"] == 0)
        & (df["wind_speed_bin"] >= min_speed)
        & (df["wind_speed_bin"] <= max_speed)
        & (df["angle_deviation_bin"].abs() <= max_abs_angle_deviation)
    ].copy()

    # Group by. Obtain mean power and number of data points per turbine,
    # wind speed bin and angle deviation bin
    df_group = (
        df.groupby(["id_wtg_complete", "wind_speed_bin", "angle_deviation_bin"])
        .agg(
            power_mean=('power', 'mean'),
            power_std=('power','std'),
            number_points=('angle_deviation','count')
        ).reset_index()
    )

    # Filter out bins with low data count
    df_group = df_group[df_group["number_points"] >= min_number_points]

    # Obtain each individual curve we need (i.e. each combination of turbine
    # and wind speed)
    df_curves_meta = df_group[["id_wtg_complete", "wind_speed_bin"]].drop_duplicates()

    # Loop in each curve
    lst_cols = ['id_wtg_complete', 'wind_speed_bin', 'angle_deviation_bin', 'power_mean', 'type']
    lst_dfs = []
    # lst_records = []
    for i, row in df_curves_meta.iterrows():

        try:
            ## Isolate the average power obtained from data points
            df_ave_aux = df_group[
                (df_group["id_wtg_complete"] == row["id_wtg_complete"])
                & (df_group["wind_speed_bin"] == row["wind_speed_bin"])
            ].copy()
            df_ave_aux['type'] = 'average'

            ## We need at least 3 points to proceed
            if len(df_ave_aux) < 3:
                continue

            lst_dfs.append(df_ave_aux[lst_cols])

            ## Fit
            popt, pcov = curve_fit(
                poly2, 
                df_ave_aux['angle_deviation_bin'], 
                df_ave_aux['power_mean'],
                bounds = ([-np.inf, -np.inf, -np.inf], [0, np.inf, np.inf]),
                sigma = df_ave_aux['power_std']
            )
            
            # Show fit
            df_fit_aux = df_ave_aux.copy()
            df_fit_aux['type'] = 'fit'
            df_fit_aux['power_mean'] = poly2(df_fit_aux['angle_deviation_bin'], popt[0], popt[1], popt[2])
            lst_dfs.append(df_fit_aux[lst_cols])
        except Exception as error:
            logging.error(f'Unable to fit {period} {row["id_wtg_complete"]} {row["wind_speed_bin"]} m/s: {error}')

    df_final = pd.concat(lst_dfs)
    df_final['period'] = period

    return df_final
