"""
acwa.data.horizon.alarms

Check temporal horizon for alarms
"""

import pandas as pd

from acwa.db import read_table_as_df, write_df_as_table

def extract_alarms_temporal_horizon_basic(config_db: dict):
    """
    Extract the "temporal horizon basic" of the alarms per turbine, i.e. the last 
    datetime from which we should recover new alarms.

    Results are written in a SQL table

    Args:
        config_db (dict): Configuration
    """

    # Read the treated_events
    df = read_table_as_df("basic_alarms", config_db, "intermediate")
    
    # Mark alarms to be filter out (ongoing alarms)
    df = df\
        .groupby('id_wtg_complete', group_keys=False)\
        .apply(mark_ongoing_overlapping_alarms)

    # Filter out ongoing alarms
    df = df[~df['ongoing_overlapped']]

    # Extract last datetimes per turbine
    df = df.groupby('id_wtg_complete').agg({'end_datetime': 'max'})
    df = df.reset_index()
    df = df.rename(columns={'end_datetime': 'horizon_datetime'})

    # Write results in intermediate table
    write_df_as_table(
        df,
        config_db,
        "intermediate",
        "alarms_horizons_basic",
        if_exists='replace',
        index=False,
    )

def mark_ongoing_overlapping_alarms(group: pd.DataFrame) -> pd.DataFrame:
    """
    Mark alarms that are ongoing, or consecutive to ongoing

    Args:
        group (pd.DataFrame): Dataframe with alarms (of a single turbine)

    Returns:
        pd.DataFrame: Dataframe with an extra column 'ongoing_overlapped'
    """

    # Sort dataframe
    group = group.sort_values(by='start_datetime', ascending = False).reset_index(drop=True)
    
    # Create new 'ongoing_overlapped' column, initially with false
    group['ongoing_overlapped'] = False
    
    # Mark ongoing=True
    group.loc[group['ongoing'], 'ongoing_overlapped'] = True
    
    # Mark events
    for i in range(1, len(group)):
        if group.loc[i-1, 'ongoing_overlapped'] and group.loc[i-1, 'start_datetime'] == group.loc[i, 'end_datetime']:
            group.loc[i, 'ongoing_overlapped'] = True
    
    return group


def extract_alarms_temporal_horizon(config_db: dict):
    """
    Extract the "temporal horizon" of the alarms per turbine, i.e. the last 
    datetime from which we should recover new alarms.

    Results are written in a SQL table

    Args:
        config_db (dict): Configuration
    """

    # Read the treated_events
    df = read_table_as_df("treated_events", config_db, "vis")
    
    # Mark alarms to be filter out (ongoing alarms)
    df = df\
        .groupby('id_wtg_complete', group_keys=False)\
        .apply(mark_ongoing_overlapping_alarms)

    # Filter out ongoing alarms
    df = df[~df['ongoing_overlapped']]

    # Extract last datetimes per turbine
    df = df.groupby('id_wtg_complete').agg({'end_datetime': 'max'})
    df = df.reset_index()
    df = df.rename(columns={'end_datetime': 'horizon_datetime'})

    # Write results in intermediate table
    write_df_as_table(
        df,
        config_db,
        "intermediate",
        "alarms_horizons",
        if_exists='replace',
        index=False,
    )