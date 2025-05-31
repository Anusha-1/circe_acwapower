"""
acwa.data.time_aggregation

Aggregate by classification periods
"""

from datetime import date, timedelta

import pandas as pd
import numpy as np


def aggregate_by_classification_labels(
    df: pd.DataFrame,
    df_wtg: pd.DataFrame,
    classification_col: str = "classification",
    classification_groups: list[str] = [
        "Failure",
        "Maintenance",
        "Out of specification",
        "Production",
    ],
    value_to_agg: str = "duration",
    first_day: date | None = None,
    coerce_to_int: bool = True
) -> pd.DataFrame:
    """
    Count duration on the different classification periods

    Args:
        df (pd.DataFrame): Alarms dataframe
        df_wtg (pd.DataFrame): Turbines dataframe config
        classification_col (str, optional): Name of classification column.
            Defaults to 'classification'.
        classification_groups (list[str], optional): Labels on the
            classification column. Defaults to ["Failure", "Maintenance",
            "Out of specification", "Production"].
        value_to_agg (str, optional): Column with the value to aggregate.
            Defaults to "duration"
        first_day (date | None, optional): First date to consider. If None, it 
            is taken from available records. Defaults to None
        coerce_to_int (bool, optional): If True, coerce result to int. 
            Defaults to True

    Returns:
        pd.DataFrame: Dataframe with duration per group for each day
    """

    # Group by and sum durations
    group_by_indices = [
        "id_wf", "id_wtg", "id_wtg_complete", "day", classification_col]
    df_group = (
        df[group_by_indices + [value_to_agg]]
        .groupby(group_by_indices)
        .sum()
        .reset_index()
    )

    # Pivot table
    df_pivot = pd.pivot_table(
        df_group,
        values=value_to_agg,
        index=["id_wf", "id_wtg", "id_wtg_complete", "day"],
        columns=classification_col,
        aggfunc="sum",
    ).reset_index()

    # Complete days
    if first_day is None:
        first_day = df_pivot["day"].min()
    last_day = df_pivot["day"].max()
    delta = last_day - first_day
    lst_complete_days = [first_day + timedelta(days=i) for i in range(delta.days + 1)]
    df_complete_days = pd.DataFrame(
        data={
            "day": lst_complete_days, 
            "tct": [24 * 60 * 60] * len(lst_complete_days)}
    )

    # Build a dataframe with days for each available turbine
    lst_df_complete_days = []
    for i, row in df_wtg.iterrows():
        df_aux = df_complete_days.copy()
        df_aux["id_wf"] = row["id_wf"]
        df_aux["id_wtg"] = row["id_wtg"]
        df_aux["id_wtg_complete"] = row["id_wtg_complete"]
        lst_df_complete_days.append(df_aux)
    df_complete_days = pd.concat(lst_df_complete_days)

    # Merge
    df = df_complete_days.merge(
        df_pivot, how="left", on=["id_wf", "id_wtg", "id_wtg_complete", "day"]
    )

    # Fill missing values
    for col in classification_groups:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0)
        df[col] = np.floor(
            pd.to_numeric(df[col], errors="coerce")
        )  # I don't know why this is sometimes necessary...
        
        if coerce_to_int:
            df[col] = df[col].astype("Int64")

    return df
