"""
acwa.data.ml_format.reliability_xy

X/y split for reliability
"""

import pandas as pd

def split_Xy_for_reliability(
        df_data: pd.DataFrame,
        group: str
) -> tuple[pd.DataFrame,pd.Series]:
    """
    Splits X/y for reliability models

    Args:
        df_data (pd.DataFrame): Data
        group (str): Id group complete

    Returns:
        - pd.DataFrame: Feature matrix
        - pd.Series: Ground truth
    """
    
    # Isolate data for particular group (models are group-wise)
    df = df_data[df_data['id_group_complete']==group].copy()
    
    # X and y split
    X = df.drop(columns=['component_temperature'])
    X= X.rename(str, axis="columns")
    y = df['component_temperature']

    return X, y
