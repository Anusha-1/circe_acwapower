"""
acwa.reliability.full_pipeline

Define the full pipeline for the reliability models
"""

from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import QuantileRegressor

from .polyfit import PolyfitTransformer
from .select import SelectTransformer
from .running_time import RunningTimeTransformer
from .power_limit import PowerLimitTransformer
from .custom_estimator import CustomEstimator

def create_reliability_pipeline(quantile: float) -> Pipeline:

    # Different initial transformers for input features
    polyfit_transformer = PolyfitTransformer(['power'], [3])
    select_transformer = SelectTransformer(['nacelle_temperature', 'ambient_temperature'])
    running_time_tansformer = RunningTimeTransformer(
        power_col='power', log_scale=True, group_by_columns=['id_wtg_complete']
    )

    # Combine features
    combined_feature_union = FeatureUnion(
        [
            ("Polynomial Power Transformer", polyfit_transformer),
            ("Select Feature Temperatures", select_transformer),
            ("Running Time", running_time_tansformer)
        ]
    )

    # Apply a Standard Scaler for these features
    scaler = StandardScaler()
    pipe = Pipeline(
        [
            ("Feature Union", combined_feature_union),
            ("Standard Scaler", scaler)
        ]
    )

    # Flag the points with positive power. Non-operative machines are not included
    power_limiter = PowerLimitTransformer(power_threshold=100)
    final_feature_union = FeatureUnion(
        [
            ("Features to use", pipe),
            ("Power Limiter", power_limiter)
        ]
    )

    # Finally, apply a custom QuantileRegression
    qr_custom = CustomEstimator(
        QuantileRegressor, default_value=None, 
        quantile=quantile, alpha=0
    )
    final_pipe = Pipeline(
        [
            ("Feature Transformation", final_feature_union),
            ("Quantile Regression", qr_custom)
        ]
    )

    return final_pipe
