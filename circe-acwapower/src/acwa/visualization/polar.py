"""
acwa.visualization.polar

Polar plots
"""

import pandas as pd
import plotly.graph_objects as go

def plot_wind_direction_dist(df: pd.DataFrame) -> go.Figure:
    """
    Plot probability density of wind direction

    Args:
        df (pd.DataFrame): Dataframe with prob for each wind direction

    Returns:
        go.Figure: Plotly figure
    """

    color = df.apply(
        lambda row: 'red' if row['wind_direction_round'] == row['mode'] else 'blue',
        axis=1
    )

    fig = go.Figure(
        go.Barpolar(
            name="Wind Direction Distribution",
            r=df['prob'],
            theta=df['wind_direction_round'],
            marker_color=color
        )
    )

    fig.update_layout(
        polar = dict(
            angularaxis = dict(
                rotation = 90,
                direction = "clockwise",

            ),
            radialaxis = dict(
                showticklabels=False
            )
        )
    )

    return fig

def plot_wind_direction_dist_with_sectors(
        df: pd.DataFrame,
        df_sectors: pd.DataFrame) -> go.Figure:
    """
    Plot probability density of wind direction

    Args:
        df (pd.DataFrame): Dataframe with prob for each wind direction
        df_sectors (pd.Dataframe): Dataframe with sectors

    Returns:
        go.Figure: Plotly figure
    """

    fig = go.Figure()

    
    def __calculate_width(row):
        
        fin = row['sector_fin']
        ini = row['sector_ini']
        
        if ini > fin:
            fin += 360

        return fin - ini
    
    def __calculate_theta(row):
        fin = row['sector_fin']
        ini = row['sector_ini']
        
        if ini > fin:
            fin += 360

        theta = (ini + fin) / 2.0
        if theta > 360:
            theta -= 360

        return theta + 0.01

    df_sectors = df_sectors.copy()
    df_sectors['width'] = df_sectors.apply(
        __calculate_width, axis=1
    )
    df_sectors['theta'] = df_sectors.apply(
        __calculate_theta, axis=1
    )
    color = df_sectors.apply(
        lambda row: 'green' if row['sector_name'].startswith("Sector")  else 'orange',
        axis=1
    )

    fig.add_trace(
        go.Barpolar(
            name="Sectors",
            r=[df['prob'].max()*1.05] * len(df_sectors),
            theta=df_sectors['theta'],
            width=df_sectors['width'],
            text=df_sectors['sector_name'],
            hovertemplate="%{text}<extra></extra>",
            marker_color=color,
            opacity=0.5
        )
    )

    df = df.sort_values(by='wind_direction_round')

    fig.add_trace(
        go.Scatterpolar(
            name="Wind Direction Distribution",
            r=df['prob'],
            theta=df['wind_direction_round'],
            mode='lines',
            line_color='blue',
            fill='toself',
            hovertemplate="Direction: %{theta:.2f} <br>Probability: %{y:.2f}<extra></extra>"
        )
    )   

    fig.update_layout(
        polar = dict(
            angularaxis = dict(
                rotation = 90,
                direction = "clockwise",

            ),
            radialaxis = dict(
                showticklabels=False,
                ticks=""
            )
        )
    )

    return fig
