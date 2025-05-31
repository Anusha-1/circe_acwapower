"""
acwa.reliability.power_limit

Custom transformer to create a boolean column that we will use to only fit a 
model above a certain power threshold
"""

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class PowerLimitTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, power_threshold: float = 0, power_col: str = 'power'):

        self.power_threshold = power_threshold
        self.power_col = power_col

    def fit(self, X: pd.DataFrame, y: Any = None):
        """
        Fit method
        
        Args:
            X (pd.DataFrame): Feature Matrix
            y (Any, optional): Target (not necessary). Defaults to None.
        
        Returns:
            self
        """

        assert self.power_col in X.columns, f"{self.power_col} not in dataframe"

        return self
    
    def transform(self, X: pd.DataFrame, y: Any = None) -> pd.DataFrame:
        """
        Transform method

        Args:
            X (pd.DataFrame): Feature matrix
            y (Any, optional): Target (not necessary). Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with running time feature
        """

        X_ = X.copy()

        X_['data_to_use'] = X_[self.power_col] > self.power_threshold
        X_['data_to_use'] = X_['data_to_use'].fillna(False)

        return X_['data_to_use'].to_frame()
