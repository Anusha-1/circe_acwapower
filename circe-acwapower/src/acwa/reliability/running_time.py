"""
acwa.reliability.running_time

Custom transformer to obtain running time
"""

import math
from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class RunningTimeTransformer(BaseEstimator, TransformerMixin):

    def __init__(
        self, 
        power_col: str = 'power', 
        log_scale: bool = False, 
        group_by_columns: list[str] = ['id_wtg_complete']
        ):

        self.power_col = power_col
        self.log_scale = log_scale
        self.group_by_columns = group_by_columns

    def fit(self, X: pd.DataFrame, y: Any = None):
        """
        Fit method

        Args:
            X (pd.DataFrame): Feature matrix
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
        X_['bool'] = X[self.power_col] > 0
        X_['running_time'] = X_\
            .groupby(self.group_by_columns)['bool']\
            .transform(self.count_consecutive_trues) * (1.0/6.0)

        if self.log_scale:
            X_['running_time'] = X_['running_time'].apply(
                lambda x: math.log10(x) if x > 0 else None)

        return X_['running_time'].to_frame()
    
    def get_feature_names_out(self, input_features=None) -> list[str]:
        return ['running_time']

    def count_consecutive_trues(self, boolean_series: pd.Series) -> list:
        """
        Auxiliary function to count consecutive trues in a boolean series

        Args:
            boolean_series (pd.Series): 

        Returns:
            list: Consecutive trues counter
        """

        counter = 0
        result = []
        for value in boolean_series:
            if value:
                counter += 1
            else:
                counter = 0
            result.append(counter)
        return result
