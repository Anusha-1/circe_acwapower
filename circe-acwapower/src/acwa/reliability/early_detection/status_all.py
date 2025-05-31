"""
acwa.reliability.early_detection.status_all

Module to apply the early detection system to all turbines loaded in the system
"""

import pandas as pd

from .analyze import analyze_recent_reliability_data
from .data import obtain_data_for_reliability_status
from .period import obtain_min_timestamp_for_reliability_status

def apply_early_detection(
        df_status: pd.DataFrame, config_db: dict) -> pd.DataFrame:
    """
    Detect early alarms due to overtemperature

    Args:
        df_status (pd.DataFrame): Status dataframe calculated so far. Needed 
            columns: id_wf, timestamp 
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Status dataframe with early detection column
    """

    lst_wfs = list(set(df_status['id_wf']))
    lst_updated_status_df = []
    for wf in lst_wfs:
        df_status_aux = df_status[df_status['id_wf']==wf].copy()

        min_timestamp = obtain_min_timestamp_for_reliability_status(
            df_status_aux)
        
        df_rel = obtain_data_for_reliability_status(
            config_db, min_timestamp, df_status_aux, wf
        )
        
        df_wtg_rel = analyze_recent_reliability_data(config_db, df_rel)

        df_status_aux = df_status_aux.merge(
            df_wtg_rel,
            on = 'id_wtg_complete',
            how = 'left'
        )

        # In case of not having enough points to analyze, we wont obtain a 
        # reliable status. We fill those instances as True 
        df_status_aux['reliable'] = df_status_aux['reliable'].fillna(True)
        
        lst_updated_status_df.append(df_status_aux)

    return pd.concat(lst_updated_status_df)
