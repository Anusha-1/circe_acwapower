"""
acwa.visualization.plot_all

Function to replicate a turbine plot for all turbines 
"""

import pandas as pd
import plotly.graph_objects as go

def plot_all_turbines(
        dfs: pd.DataFrame | list[pd.DataFrame], 
        plot_function: callable, 
        turbine_id_col: str = 'id_wtg',
        **kwargs) -> go.Figure:
    """
    Take a plot function that works at the level of turbine, and replicate for
    different turbines with a dropdown selector

    Args:
        dfs (pd.DataFrame | list[pd.DataFrame]): Dataframe(s) with column to 
            select turbine ('id_wtg')
        plot_function (callable): Function plot for turbine
        **kwargs: Kwargs for plot function

    Returns:
        go.Figure: Plotly Figure
    """

    if isinstance(dfs, list):
        df = dfs[0]
    else:
        df = dfs
        dfs = [df]


    list_turbines = list(set(df[turbine_id_col]))
    list_turbines.sort()

    # Initial traces (turbine 1)
    args = [df[df[turbine_id_col]==list_turbines[0]] for df in dfs]
    fig = plot_function(*args, **kwargs)
    visible_array = [True] * len(fig.data)
    traces_index_per_turbine = [(0, len(fig.data))]
    current_number_of_traces = len(fig.data)

    # Extend figures
    
    for turbine in list_turbines[1:]:
        trace_counter = 0
        args = [df[df[turbine_id_col]==turbine] for df in dfs]
        fig_aux = plot_function(*args, **kwargs)

        for trace in fig_aux.data:
            fig.add_trace(trace)
            visible_array.append(False)
            trace_counter += 1

        traces_index_per_turbine.append((current_number_of_traces, current_number_of_traces+trace_counter))
        current_number_of_traces += trace_counter

    # Visible arrays per turbine
    buttons = []
    for i, turbine in enumerate(list_turbines):
        visible_array_aux = [False] * len(visible_array)
        for index in range(traces_index_per_turbine[i][0], traces_index_per_turbine[i][1]):
            visible_array_aux[index] = True

        buttons.append(
            dict(
                label=f"Turbine {turbine}",
                method='update',
                args=[{"visible": visible_array_aux}]
            )
        )

    for i, trace in enumerate(fig.data):
        trace["visible"] = visible_array[i]

    fig.update_layout(updatemenus=[dict(active=0, buttons=buttons)])
    fig.update_layout()
    fig.update_layout(
        title="Khalladi",
    )

    return fig