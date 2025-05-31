"""
acwa.yaw.dynamic.hour_counts

Module to count directional changes per hour
"""

from datetime import datetime

import pandas as pd

from acwa.yaw.dynamic.hour_reference_counts import count_directional_reference_changes

def count_directional_changes(
        df: pd.DataFrame,
        lst_col: list[str] = [
            'wind_direction_change', 
            'nacelle_direction_change'
            ],
        lst_labels: list[str] = [
            'Wind Direction',
            'Nacelle Direction'
        ]
) -> pd.DataFrame:
    """
    Count directional changes per hour

    Args:
        df (pd.DataFrame): 1min data
        lst_col (list[str], optional): List of columns with directional changes
            to consider. These must be boolean columns. Defaults to 
            ['wind_direction_change', 'nacelle_direction_change'].
        lst_labels (list[str], optional): Label for each directional field. 
            Defaults to [ 'Wind Direction', 'Nacelle Direction'].

    Returns:
        pd.DataFrame: New dataframe with 'id_wtg_complete', 'hour', 'changes'
            and 'label'
    """
    
    ## Wind and Nacelle changes per turbine
    df['hour'] = df['timestamp'].apply(
        lambda x: datetime(x.year, x.month, x.day, x.hour, 0, 0))    
    agg_dict = {col:"sum" for col in lst_col}
    agg_dict['timestamp'] = 'count'
    df_group = df\
        .groupby(['id_group_complete','id_wtg_complete', 'hour'])\
        .agg(agg_dict)\
        .reset_index()\
        .rename(columns={
            "timestamp": "total_seconds_of_data"
            }
        )

    ## Filter only cases with count = 60
    df_group = df_group[df_group['total_seconds_of_data'] == 60]

    ## Obtain the reference, and merge
    df_group_ref = count_directional_reference_changes(df)
    lst_col.append("reference_change")
    lst_labels.append("Reference")
    df_group = df_group.merge(
        df_group_ref[['id_group_complete','hour', 'reference_change']],
        on=['id_group_complete','hour'],
        how='left'
    )

    ## Prepare table
    lst_dfs = []
    for col, label in zip(lst_col, lst_labels):
        df_aux = df_group[['id_wtg_complete', 'hour', col]].rename(
            columns={col: "changes"})
        df_aux['label'] = label
        lst_dfs.append(df_aux)

    return pd.concat(lst_dfs)
