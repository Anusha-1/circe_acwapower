"""
acwa.alarms.priority.overlap_all

Module to clean overlaps at all turbines
"""

import pandas as pd

from acwa.alarms.priority.overlap_turbine import avoid_overlapping_alarms_in_turbine

def avoid_overlapping_alarms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe with all the alarms, and cleans it by removing overlaps

    Args:
        df (pd.DataFrame): Original Dataframe

    Returns:
        pd.DataFrame: Corrected dataframe
    """

    lst_turbines = list(set(df['id_wtg_complete']))
    lst_dfs = []
    for turb in lst_turbines:
        df_aux = avoid_overlapping_alarms_in_turbine(df[df['id_wtg_complete']==turb])
        lst_dfs.append(df_aux)

    return pd.concat(lst_dfs, ignore_index=True)
