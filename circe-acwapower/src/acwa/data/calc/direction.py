"""
acwa.data.calc.direction

Calculations on directions
"""

import pandas as pd

def obtain_main_direction(df:pd.DataFrame) -> pd.DataFrame:
    """
    Obtain main direction of wind from 10min data

    Args:
        df (pd.DataFrame): 10min data

    Returns:
        pd.DataFrame: Dataframe with main direction (mode) per turbine
    """

    df['wind_direction_round'] = df['wind_direction'].round()
    df_mode = df.groupby(['id_wtg']).agg(
        {"wind_direction_round": (pd.Series.mode, "count")})
    df_mode.columns = df_mode.columns.droplevel(0)
    df_mode = df_mode.rename(columns={"count": "total"}).reset_index()

    return df_mode

def obtain_distribution_of_directions(
        df: pd.DataFrame,
        df_mode: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Obtain prob distribution of wind directions

    Args:
        df (pd.DataFrame): Dataframe of 10min data
        df_mode (pd.DataFrame | None, optional): Dataframe with main directions.
            Defaults to None.

    Returns:
        pd.DataFrame: Dataframe with distribution
    """

    if df_mode is None:
        df_mode = obtain_main_direction(df)

    # Obtain directions
    df_directions = df.groupby(['id_wtg', 'wind_direction_round']).agg(
        {"wind_direction_round": "count"}
    ).rename(columns = {"wind_direction_round": "count"}).reset_index()

    # Merge and complete data
    df_directions = df_directions.merge(df_mode, on="id_wtg")
    df_directions['prob'] = df_directions['count']/df_directions['total']

    return df_directions