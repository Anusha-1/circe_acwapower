"""
acwa.oper.lambda_parameter

Module to obtain lambda (tip-speed ratio)
"""

import numpy as np
import pandas as pd

def calculate_lambda(
        df_10min: pd.DataFrame, wtg_config: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate lambda (tip-speed ratio) as:

        lambda = rotor RPM x radius / wind speed

    Args:
        df_10min (pd.DataFrame): Dataframe with columns: 'rotor_rpm' and 
            'wind_speed'
        wtg_config (pd.DataFrame): Dataframe with WTG configuration. It has the
            rotor diameter, which allows us to obtain the radius

    Returns: 
        (pd.DataFrame): Dataframe with lambda calculated in extra column:
            'lambda_parameter'
    """

    # Merge radius
    wtg_config["radius"] = (wtg_config["rotor_diameter"] / 2)
    df_10min = pd.merge(
        df_10min, 
        wtg_config[["id_wtg_complete", "radius"]], 
        on="id_wtg_complete"
    )

    # Apply formula
    df_10min['lambda_parameter'] = df_10min['rotor_rpm']*(2*np.pi/60)* df_10min['radius']/df_10min['wind_speed']
    
    # Format incorrect values
    df_10min['lambda_parameter'] = np.maximum(0, df_10min['lambda_parameter'])
    df_10min['lambda_parameter'] = np.minimum(100, df_10min['lambda_parameter'])
    
    return df_10min
