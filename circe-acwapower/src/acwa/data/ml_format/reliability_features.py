"""
acwa.data.ml_format.reliability_features

Feature engineering for reliability Quantile Regression
"""

import pandas as pd

def format_features_for_reliability(
    df_data: pd.DataFrame, signal: str, 
) -> pd.DataFrame:
    """
    Prepare dataframe for reliability QR models

    Args:
            df_data (pd.DataFrame): Full data
            signal (str): Signal to evaluate

    Returns:
            pd.DataFrame: Formatted dataframe
    """

    # Rename the signal to study as "component_temperature"
    df_aux = df_data.rename(
        columns={
            signal: "component_temperature",
        }
    )

    return df_aux.copy()
