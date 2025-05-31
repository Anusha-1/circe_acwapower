"""
acwa.alarms.component.complete

Module to complete with missing turbine-components
"""

import itertools

import pandas as pd

def complete_info_per_turbine_component(
        lst_wtgs: list[str], 
        lst_components: list[str],
        df_current_alarms: pd.DataFrame) -> pd.DataFrame:
    """
    Complete information on current alarms per turbine-component so no pair of 
    turbine-component is missed in the dataframe

    Args:
        lst_wtgs (list[str]): List of all turbines
        lst_components (list[str]): List of all components
        df_current_alarms (pd.DataFrame): Current alarms (incomplete)

    Returns:
        pd.DataFrame: Current alarms (complete)
    """


    lst_records = []
    for wtg, component in itertools.product(lst_wtgs, lst_components):
        lst_records.append(
            {
                "id_wtg_complete": wtg,
                "component": component
            }
        )
    df_full_info = pd.DataFrame.from_records(lst_records).merge(
        df_current_alarms[['id_wtg_complete', 'component', 'code', 'description']],
        on=['id_wtg_complete','component'],
        how='left'
    )
    df_full_info['code'] = df_full_info['code'].fillna(0)
    df_full_info['description'] = df_full_info['description'].fillna("Running")

    return df_full_info
