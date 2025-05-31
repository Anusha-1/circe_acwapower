"""
acwa.reliability.polyfit

Custom transformer for fitting features to polynomial 
"""

from typing import Callable

import pandas as pd
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, TransformerMixin

from .polynomial_function import build_polynomial_function

class PolyfitTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, feature_names: list[str], degrees: list[int]):
        """
        Initialization method

        Args:
            feature_names (list[str]): List of features to fit
            degrees (list[int]): List of degrees for the polynomial considered 
                for each feature
        """

        assert len(feature_names) == len(degrees), \
            "Size of feature names and degrees don't match"
        
        self.feature_names = feature_names
        self.degrees = degrees
        self.fitted_coefficients : list[list[float]] = []
        self.functions: list[Callable] = []

        self.feature_names_out: list[str] = []

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit method

        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target to fit

        Returns:
            self
        """

        self.fitted_coefficients : list[list[float]] = []
        self.functions: list[Callable] = []
        for feat, degree in zip(self.feature_names, self.degrees):

            function_to_fit = build_polynomial_function(degree)

            ## Drop Na
            df_aux = pd.concat([X[feat],y], axis=1)
            df_aux.columns = ['feature', 'target']
            df_aux = df_aux.dropna()

            popt, pcov = curve_fit(
                function_to_fit, df_aux["feature"], df_aux["target"]
            )

            self.fitted_coefficients.append(popt)
            self.functions.append(function_to_fit)

        return self

    def transform(self, X: pd.DataFrame, y: None = None) -> pd.DataFrame:
        """
        Transform method

        Args:
            X (pd.DataFrame): Feature matrix
            y (None, optional): Target (needed for consistency). 
                Defaults to None.

        Returns:
            pd.Dataframe: Dataframe with the final features
        """

        X_ = X.copy()
        lst_final_features = []
        for feat, popt, function in zip(self.feature_names, self.fitted_coefficients, self.functions):

            final_feature_name = f"{feat}_poly"

            tuple_popt = tuple(popt)

            X_[final_feature_name] = X_[feat].apply(
                function, args=tuple_popt
            )

            lst_final_features.append(final_feature_name)

        self.feature_names_out = lst_final_features

        return X_[lst_final_features]
    
    def get_feature_names_out(self, input_features=None) -> list[str]:
        return self.feature_names_out
