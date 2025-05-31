"""
acwa.yaw.dynamic.hour_reference_counts

Module to count average directional changes per hour and group of turbines
"""

import pandas as pd

def count_directional_reference_changes(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count directional changes per hour (for reference)

    Args:
        df (pd.DataFrame): 1min data

    Returns:
        pd.DataFrame: Grouped dataframe
    """

    ## Sum of changes per group
    df = df.dropna(subset='nacelle_direction_change')

    agg_dict = {
        'nacelle_direction_change': 'sum',
        'id_wtg_complete': 'nunique',
        'timestamp': 'nunique'
    }

    df_group = df\
        .groupby(['id_group_complete', 'hour'])\
        .agg(agg_dict)\
        .reset_index()\
        .rename(columns={
            'id_wtg_complete': 'total_turbines',
            'timestamp': 'total_seconds_of_data',
            'nacelle_direction_change': 'reference_change'
        })

    ## Divide by the number of turbines with data
    df_group['reference_change'] = df_group['reference_change'] / df_group['total_turbines']
    
    ## Filter data
    df_group = df_group[df_group['total_seconds_of_data'] == 60]

    return df_group
