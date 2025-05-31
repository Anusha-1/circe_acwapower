"""
acwa.reliability.predict

Module to perform predictions with reliability models
"""

import pathlib

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

import acwa.files as files

def predict_reliability(
        X_features: pd.DataFrame,
        signal: str,
        group: str,
        oper_stat: str,
        config_file: dict
) -> np.ndarray:
    """
    Opens a saved model, and use it to predict

    Args:
        X_features (pd.DataFrame): Input features
        signal (str): Temperature signal
        group (str): Group
        oper_stat (str): Statistic to fit (median, upper bound or lower bound)
        config_file (dict): Configuration of file storage

    Returns:
        np.ndarray: Predictions made
    """
    
    path_to_model = pathlib.Path(
        "output", "qr_models",
        f"{signal}_{group}_{oper_stat}.pkl"
    )

    qr: Pipeline = files.read_pickle(
        path_to_model, config_file, 'data')
    
    return qr.predict(X_features)
    