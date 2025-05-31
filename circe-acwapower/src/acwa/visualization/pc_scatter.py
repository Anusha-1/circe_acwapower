"""
acwa.visualization.pc_scatter

Plot scatter power curves
"""

import pandas as pd
import plotly.graph_objects as go

COLORS = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4' ]

def plot_power_vs_speed_sector(df: pd.DataFrame) -> go.Figure:
    """
    Plot power vs speed, differentiating the sector

    Args:
        df (pd.DataFrame): 10min data

    Returns:
        go.Figure: Plotly figure
    """


    fig = go.Figure()


    df_group_sectors = df.groupby(['sector_name']).agg({"power": "count"}).reset_index()
    df_group_sectors = df_group_sectors.sort_values(by='power', ascending=False)
    sectors = list(df_group_sectors['sector_name'])

    for sector in sectors:

        df_aux = df[df['sector_name']==sector]

        fig.add_trace(
            go.Scatter(
                name=f"{sector}",
                x=df_aux['wind_speed_corrected'],
                y=df_aux['power'],
                mode="markers",
                marker=dict(
                    line_width=0,
                    size=2
                    ),
                legendgroup=sector
            )
        )

    fig.update_layout(xaxis_title="Wind Speed (Corrected)", yaxis_title="Power")

    return fig

def plot_power_vs_speed_sector_with_bin(
        df: pd.DataFrame,
        df_pc: pd.DataFrame) -> go.Figure:
    """
    Plot power vs speed, differentiating the sector + binned curve

    Args:
        df (pd.DataFrame): 10min data
        df_pc (pd.DataFrame): Curves

    Returns:
        go.Figure: Plotly figure
    """


    fig = go.Figure()


    df_group_sectors = df.groupby(['sector_name']).agg({"power": "count"}).reset_index()
    df_group_sectors = df_group_sectors.sort_values(by='power', ascending=False)
    sectors = list(df_group_sectors['sector_name'])

    color_index = 0
    for sector in sectors:

        df_aux = df[df['sector_name']==sector]
        df_pc_aux = df_pc[df_pc['sector_name']==sector]

        fig.add_trace(
            go.Scatter(
                name=f"{sector} data points",
                x=df_aux['wind_speed_corrected'],
                y=df_aux['power'],
                mode="markers",
                marker=dict(
                    line_width=0,
                    size=0.5,
                    color=COLORS[color_index]
                    ),
                legendgroup=sector,
                hoverinfo="skip"
            )
        )

        fig.add_trace(
            go.Scatter(
                name=f"{sector} calculated curve",
                x=df_pc_aux['bin'],
                y=df_pc_aux['power'],
                mode="lines",
                line=dict(
                    color=COLORS[color_index]),
                legendgroup=sector,
                hovertemplate="Power: %{y:.2f}"
            )
        )

        color_index += 1

    fig.update_layout(
        xaxis_title="Wind Speed (Corrected)", 
        yaxis_title="Power",
        hovermode="x unified")

    return fig