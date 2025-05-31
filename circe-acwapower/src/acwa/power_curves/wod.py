"""
acwa.power_curves.wod

Module to use wod to generate a power curve
"""

import pathlib

import pandas as pd
import plotly.graph_objects as go

from wod.wind_turbine import WindTurbine

def generate_power_curve_with_wod(
        df: pd.DataFrame,
        name: str | None = None,
        plot: bool = False,
        config_file: dict | None = None,
        freq: str = '10min') -> pd.DataFrame:
    """
    Generate a Power Curve using the WOD package

    Args:
        df (pd.DataFrame): Power vs Speed data to use
        name (str | None, optional): Name for the Wind Turbine object. 
            Defaults to None.
        plot (bool, optional): Plot Power Curves. Default to False
        config_file (dict | None, optional): File Storage configuration. 
            Only needed if plot is True
        freq (str, optional): Frequency of the data. Defaults to '10min'.

    Returns:
        pd.DataFrame: Dataframe with Power Curve, columns bin, power, sigma
    """

    wt = WindTurbine(
        name = name,
        data = df,
        error_threshold=101
    )

    wt.create_power_curves(
        list_metadata=[{'type': 'global'}],
        algorithm_kwargs=dict(
            minimum_numer_of_bins=5,
            min_deviation_after_elbow=30))
    
    if plot:
        fig: go.Figure = wt.plot(
            plot_type='basic', power_curve_index=[0], max_bin=25.0, hover=False)
        
        ## Only Local
        folder_path = pathlib.Path(
            config_file['root_path'], "data", "output", "power_curves",
        )
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = pathlib.Path(folder_path, f"{name}_{freq}.html")
        fig.write_html(
            file_path, include_plotlyjs='cdn', full_html=False 
        )

    
    return wt.power_curves[0]\
        .data[['bin','power','deviation']]\
        .copy()\
        .rename(columns={'deviation': 'sigma'})  
