"""
acwa.reliability.coefficients

Module to obtain the fitted coefficients on a reliability pipeline
"""

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler

from .polyfit import PolyfitTransformer
from .custom_estimator import CustomEstimator

def extract_coefficients(pipe: Pipeline) -> dict:

    # Extract coefficients from polyfit transformer
    feature_union_external: FeatureUnion = pipe[0]
    feature_union_internal: FeatureUnion = feature_union_external.transformer_list[0][1][0]
    polyfit_transformer: PolyfitTransformer = feature_union_internal.transformer_list[0][1]
    polyfit_coef_dict = {
        "polynomial_fit_coef_3": polyfit_transformer.fitted_coefficients[0][0],
        "polynomial_fit_coef_2": polyfit_transformer.fitted_coefficients[0][1],
        "polynomial_fit_coef_1": polyfit_transformer.fitted_coefficients[0][2],
        "polynomial_fit_offset": polyfit_transformer.fitted_coefficients[0][3]
    }

    # Extract coefficients from standard scaler
    standard_scaler: StandardScaler = feature_union_external.transformer_list[0][1][1]
    ss_coef_dict = {
        "power_avg": standard_scaler.mean_[0],
        "power_var": standard_scaler.var_[0],
        "nacelle_temperature_avg": standard_scaler.mean_[1],
        "nacelle_temperature_var": standard_scaler.var_[1],
        "ambient_temperature_avg": standard_scaler.mean_[2],
        "ambient_temperature_var": standard_scaler.var_[2],
        "running_time_avg": standard_scaler.mean_[3],
        "running_time_var": standard_scaler.var_[3]
    }

    # Extract coefficients from QuantileRegressor
    qr: CustomEstimator = pipe[-1]
    qr_coef_dict = {
        'qr_power_coefficient': qr.estimator.coef_[0],
        'qr_nacelle_temperature_coefficient': qr.estimator.coef_[1],
        'qr_ambient_temperature_coefficient': qr.estimator.coef_[2],
        'qr_running_time_coefficient': qr.estimator.coef_[3],
        'qr_offset': qr.estimator.intercept_
    } 

    return {**polyfit_coef_dict, **ss_coef_dict, **qr_coef_dict}
