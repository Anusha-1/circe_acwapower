"""
acwa.reliability.select

Custom transformer to select features
"""

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class SelectTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, feature_names: list[str]):
        """
        Initialization method

        Args:
            feature_names (list[str]): List of features to select
        """

        self.feature_names = feature_names

    def fit(self, X: pd.DataFrame, y: Any = None):
        """
        Fit method. This is not really necessary for this transformer, as we
        don't have to fit anything. But we will use it to do a check.

        Args:
            X (Any, optional): Feature matrix (not necessary). Defaults to None.
            y (Any, optional): Target (not necessary). Defaults to None.

        Returns:
            self
        """
        
        lst_missing_features = []
        for feat in self.feature_names:

            if feat not in X.columns:
                lst_missing_features.append(feat)


        assert len(lst_missing_features) == 0,\
            f"Following features are missing from the data: {lst_missing_features.join(', ')}"

        return self

    def transform(self, X: pd.DataFrame, y: None = None) -> pd.DataFrame:
        """
        Transform method

        Args:
            X (pd.DataFrame): Feature matrix
            y (None, optional): Target (only defined here for consistency). 
                Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with selected features
        """

        X_ = X.copy()

        return X_[self.feature_names]
    
    def get_feature_names_out(self, input_features=None) -> list[str]:
        return self.feature_names
    