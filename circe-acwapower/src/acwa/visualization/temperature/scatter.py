"""
acwa.visualization.temperature.scatter

Plot scatter temp vs power
"""

import pandas as pd
import plotly.graph_objects as go


def plot_temp_vs_power(
        df: pd.DataFrame, 
        lst_temp_cols: list[str] | None = None, 
        group: str = "grid", 
        samples: int = 1000) -> go.Figure:
    """
    Plot temperature vs power

    Args:
        df (pd.DataFrame): Dataframe
        lst_temp_cols (list[str] | None, optional): List of temp columns. 
            Defaults to None.
        group (str, optional): Group. 
            Defaults to "grid".
        samples (int, optional): Number of samples. Defaults to 1000.

    Returns:
        go.Figure: Plotly figure
    """
    
    df = df.sample(samples)

    fig = go.Figure()

    lst_temp_cols = list(filter(lambda x: x.startswith(group), lst_temp_cols))

    for temp in lst_temp_cols:

        fig.add_trace(
            go.Scatter(
                x=df['grid_power'],
                y=df[temp],
                name=temp,
                mode = 'markers'
            )
        )

    fig.update_xaxes(title_text='Power (kW)')
    fig.update_yaxes(title_text="Temperature (º)")
    fig.update_layout(title_text=group)

    return fig
