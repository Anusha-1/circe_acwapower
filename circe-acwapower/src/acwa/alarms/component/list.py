"""
acwa.alarms.component.list

Module to extract a clean list of components
"""

import acwa.db as db

import pandas as pd

def get_list_of_components(
        config_db: dict,
        df_alarms_metadata: pd.DataFrame | None = None,
        df_temp_signals: pd.DataFrame | None = None) -> list[str]:
    """
    Get full list of components

    Args:
        config_db (dict): Configuration of database
        df_alarms_metadata (pd.DataFrame | None, optional): Dataframe with 
            alarms metadata. If None, it will read the data from the database.
            Defaults to None.
        df_temp_signals (pd.DataFrame | None, optional): Dataframe with 
            temperature signals. If None, it will read the data from the database.
            Defaults to None.

    Returns:
        list[str]: List of components
    """

    if df_alarms_metadata is None:
        df_alarms_metadata = db.read_table_as_df(
            "alarms_metadata", config_db, "vis"
        )
    if df_temp_signals is None:
        df_temp_signals = db.read_table_as_df(
            "temperature_signals", config_db, "vis"
        )
    lst_components = list(
        set(df_alarms_metadata["component"]).union(set(df_temp_signals["main_component"]))
    )
    lst_components.sort()

    return lst_components
