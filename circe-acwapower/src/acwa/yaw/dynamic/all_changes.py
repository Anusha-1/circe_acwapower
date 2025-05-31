"""
acwa.yaw.dynamic.all_changes

Module to count directional changes
"""

import pandas as pd

from acwa.yaw.dynamic.single_change import mark_single_directional_change

def mark_all_directional_changes(
        df: pd.DataFrame,
        directional_columns : list[str] = [
            'wind_direction', 'nacelle_direction'],
        turbine_column: str = 'id_wtg_complete',
        change_threshold: float = 1.0
) -> pd.DataFrame:
    """
    Mark with boolean columns the rows for which there are a directional change
    with respect to the previous timestamp.

    Args:
        df (pd.DataFrame): Dataframe with 1min data
        directional_columns (list[str], optional): List of columns with 
            directions to consider. Defaults to [ 'wind_direction', 
            'nacelle_direction', 'angle_deviation'].
        turbine_column (str, optional): Name of the column with turbines id. 
            Default to 'id_wtg_complete'
        change_threshold (float, optional): Minimum change needed to be considered.
            Defaults to 1.0

    Returns:
        pd.DataFrame: Dataframe with extra columns
    """

    df = df.sort_values(by=[turbine_column, 'timestamp'])

    for col in directional_columns:
        prev_col = f'{col}_prev'
        df[prev_col] = df.groupby(turbine_column)[col].shift(1)

        change_col = f'{col}_change'
        df[change_col] = df.apply(
            mark_single_directional_change,
            args = (col, prev_col, change_threshold),
            axis = 1
        )

        df.drop(columns=[prev_col])

    return df
