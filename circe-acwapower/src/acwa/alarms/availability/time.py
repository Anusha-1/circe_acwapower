"""
acwa.alarms.availability.time

Module to apply all different time-based availabilites
"""

import pandas as pd

import acwa.alarms.availability.time_formulas as time_formulas
from acwa.data import extend_by_days, aggregate_by_classification_labels

def obtain_time_based_availabilities(
    df: pd.DataFrame, 
    df_wtg: pd.DataFrame, 
    df_daily_wind: pd.DataFrame,
    df_maint: pd.DataFrame
) -> pd.DataFrame:
    """
    Obtain availabilities

    Args:
        df (pd.DataFrame): Dataframe with priority alarms
        df_wtg (pd.DataFrame): Dataframe with wtg config
        df_daily_wind (pd.DataFrame): Dataframe with daily wind
            (wind_time_seconds)
        df_maint (pd.DataFrame): Dataframe with maintenance information

    Returns:
        pd.DataFrame: Dataframe with availabilities per turbine and day
    """

    lst_availabilities = [        
        "wind",
        "operation_I",
        "operation_II",
        "operation_III",
        "technical",
        "contractual"
    ]

    ## Extend by days
    df = extend_by_days(df)
    df["day"] = df["start_datetime"].apply(lambda x: x.date())

    ## Merge with maintenace asof
    df = df.sort_values(by='start_datetime')
    df_maint = df_maint.sort_values(by='end_datetime')\
        .rename(columns={"end_datetime": "maint_end_datetime"})
    
    df = pd.merge_asof(
        df,
        df_maint[['id_wtg_complete', 'maint_end_datetime', 'cumulative_duration_hours']],
        by='id_wtg_complete',
        left_on='start_datetime',
        right_on='maint_end_datetime',
        direction="backward",
    )

    ## Reassign alarms priority to account for maintenance hours
    def reassign_maintenance(row):
        if row['classification'] == 'Maintenance':
            if row['cumulative_duration_hours'] > 80 and row['priority'] not in [8,9,10]:
                return 9 # Maintenance time considered as unavailable 
            elif row['cumulative_duration_hours'] < 80 and row['priority'] in [8,9,10]:
                return 7 # Maintenance time considered as available            
        
        return row['priority']
    df['contractual_priority'] = df.apply(reassign_maintenance, axis=1)

    ## Count time per priority group
    df_agg = aggregate_by_classification_labels(
        df, df_wtg, first_day=df_daily_wind["day"].min(), 
        classification_col="priority",
        classification_groups=list(range(1,13))
    )

    
    ## Unassigned time in 1
    unassigned_time = df_agg['tct']
    for j in range(1,13):
        unassigned_time = unassigned_time - df_agg[j]
    df_agg[1] = df_agg[1] + unassigned_time

    df_agg = df_agg.merge(
        df_daily_wind[["id_wtg_complete", "day", "wind_time_seconds"]],
        on=["id_wtg_complete", "day"],
    ).rename(columns={'wind_time_seconds': 'wind'})

    ## Add time per contractual priority group
    df_agg_cont = aggregate_by_classification_labels(
        df, df_wtg, first_day=df_daily_wind["day"].min(), 
        classification_col="contractual_priority",
        classification_groups=list(range(1,13))
    ).drop(columns=['tct','id_wf','id_wtg']).rename(
        columns={x:f"{x}_contractual" for x in range(1,13)}
    )

    df_agg = df_agg.merge(
        df_agg_cont,
        on=['day','id_wtg_complete'],
        how='left'
    )

    ## Unassigned time in "1_contractual"
    unassigned_time = df_agg['tct']
    for j in [f"{x}_contractual" for x in range(1,13)]:
        unassigned_time = unassigned_time - df_agg[j]
    df_agg["1_contractual"] = df_agg["1_contractual"] + unassigned_time

    ## Obtain availabilities
    for avail in lst_availabilities:
        df_agg = getattr(time_formulas, f"apply_{avail}_availability")(df_agg)

    return df_agg
