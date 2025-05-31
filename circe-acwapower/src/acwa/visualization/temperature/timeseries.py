"""
acwa.visualization.temperature

Plot temperature timeseries
"""

import pandas as pd
import plotly.graph_objects as go

def plot_temp_time_series(
        df: pd.DataFrame, temp_col: str = 'ambient_temperature') -> go.Figure:
    """
    Plot Temparture time series

    Args:
        df (pd.DataFrame): Dataframe of one turbine
        temp_col (str): Temperature to represent

    Returns:
        go.Figure: Plotly figure
    """

    fig = go.Figure(
        go.Scatter(
            x=df['datetime'],
            y=df[temp_col],
            mode="lines"
        )
    )

    fig.update_xaxes(title_text='Timestamp')
    fig.update_yaxes(title_text="Temperature (º)")
    fig.update_layout(title_text=temp_col)

    return fig
