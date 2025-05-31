"""
acwa.oper.cp

Module for Cp calculation
"""

import pandas as pd
import numpy as np

def calculate_cp_10min(
    df_10min: pd.DataFrame, wtg_config: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate cp using the formula:
        
        cp = power/(1/2*rho*section*(wind_speed)^3)

    in a dataframe
        
    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data. Necesary columns:
            'power', 'density', 'id_wtg_complete', 'wind_speed'
        wtg_config (pd.DataFrame): Dataframe with turbine metadata. From here we
            get the rotor diameter to calculate rotor section.

    Returns:
        pd.DataFrame: df_10min with added column of cp
    """

    # Merge section info
    wtg_config["section"] = np.pi * (wtg_config["rotor_diameter"] / 2)**2
    df_10min = pd.merge(
        df_10min, 
        wtg_config[["id_wtg_complete", "section"]], 
        on="id_wtg_complete"
    )

    # Apply formula Cp = Power/(0.5*ro*A*V**3)
    df_10min["cp"] = (
        2
        * df_10min["power"] * 1000 #kw to w
        / (df_10min["density"] * df_10min["section"] * df_10min["wind_speed"] ** 3)
    )  

    # Format incorrect values
    df_10min["cp"] = np.maximum(df_10min['cp'],0)
    df_10min.loc[df_10min["cp"] == float('-inf'), "cp"] = 0
    df_10min.loc[df_10min["cp"] == float('inf'), "cp"] = 0

    return df_10min
