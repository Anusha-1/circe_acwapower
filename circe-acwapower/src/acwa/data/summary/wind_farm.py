"""
acwa.data.summary.wind_farm

Aggregate KPIs at the level of wind farm, for a given period
"""

import pandas as pd

def sum_kpis_at_wind_farm(
        df: pd.DataFrame,
        cols_to_sum: list[str],
        period_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Sum KPIs at the level of wind farm

    Args:
        df (pd.DataFrame): Dataframe
        cols_to_sum (list[str]): Cols to sum
        period_cols (list[str] | None, optional): Columns to define the period groups. 
            If None, we consider that there are not period groups, and we only group
            at wind farm level. Defaults to None.

    Returns:
        pd.DataFrame: Grouped dataframe
    """
    
    group_cols = ['id_wf']
    if period_cols is not None:
        group_cols += period_cols
    
    df_group = df[group_cols + cols_to_sum]\
        .groupby(group_cols)\
        .sum()
    
    return df_group.reset_index().copy()
