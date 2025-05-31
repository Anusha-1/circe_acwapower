"""
acwa.visualization.temperature.distribution

Plot temperatures distributions
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors

def plot_temp_distributions(
        df: pd.DataFrame, 
        lst_temp_cols: list[str] | None = None, 
        group: str = 'grid') -> go.Figure:
    """
    Plot distribution of temperature

    Args:
        df (pd.DataFrame): Dataframe
        lst_temp_cols (list[str] | None, optional): List of temperature columns. 
            Defaults to None.
        group (str, optional): Group of temperature to analyze. 
            Defaults to 'grid'.

    Returns:
        go.Figure: Plotly figure
    """

    fig = go.Figure()    
    
    lst_temp_cols = list(filter(lambda x: x.startswith(group), lst_temp_cols))
    if len(lst_temp_cols) == 0:
        return fig
    if len(lst_temp_cols) == 1:
        colors = ['rgb(5, 200, 200)']
    else:
        colors = n_colors(
            'rgb(5, 200, 200)', 
            'rgb(200, 10, 10)', 
            len(lst_temp_cols), 
            colortype='rgb')
    
    for temp, color in zip(lst_temp_cols, colors):

        data = df[temp]
        fig.add_trace(go.Violin(x=data, line_color=color, name=temp))

    fig.update_traces(orientation='h', side='positive', width=3, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
    fig.update_yaxes(showticklabels=False)

    return fig
