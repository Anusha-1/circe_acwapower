"""
acwa.reliability.custom_estimator

Custom estimator to only be fitted, and used for prediction, in marked data points
"""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

class CustomEstimator(BaseEstimator):

    def __init__(
            self,
            estimator: BaseEstimator,
            default_value: Any = None,
            **estimator_hyperparam
    ):
        """
        Initialization method

        Args:
            estimator (BaseEstimator): Estimator to use
            default_value (Any, optional): Value to assign where we don't use
                the prediction. Defaults to None.
        """
        
        self.estimator: BaseEstimator = estimator(**estimator_hyperparam)
        self.default_value = default_value

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit method

        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target

        Returns:
            self
        """

        bool_ser = X[:,-1]

        ## Data to fit
        X_to_fit = pd.DataFrame(X[:,:-1]).copy()
        cond = (bool_ser==1) & (~X_to_fit.isna().any(axis=1)) & (~np.isnan(y.to_numpy()))        
        X_to_fit = X_to_fit[cond]
        y_to_fit = y[cond.values]

        self.estimator = self.estimator.fit(X_to_fit, y_to_fit)

        return self
    
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Predict method

        Args:
            X (pd.DataFrame): Feature matrix

        Returns:
            pd.Series: Prediction
        """

        X_ = pd.DataFrame(X).copy()

        bool_ser = X[:,-1]

        ## Data to predict
        X_to_predict = pd.DataFrame(X[:,:-1]).copy()
        cond = (bool_ser==1) & (~X_to_predict.isna().any(axis=1))         
        X_to_predict = X_to_predict[cond]
        X_.loc[cond, 'prediction'] = self.estimator.predict(X_to_predict)

        ## Default
        if self.default_value is not None:
            X_['prediction'] = X_['prediction'].fillna(value=self.default_value)

        return X_['prediction']
    
    def fit_predict(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit-predict method

        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target

        Returns:
            self
        """

        self.fit(X, y)

        return self.predict(X)
