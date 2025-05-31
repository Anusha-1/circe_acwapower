"""
acwa.alarms.availability.time_formulas.operation_II

Formula for operation availability option II
"""

import pandas as pd


def apply_operation_II_availability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the operation II availability formula:

        operation_II_availability = 1 - Unavail Time / (Avail Time + Unavail Time)

    where Available and Unavailable Time come from the following priority groups:

        Available: 1, 2 and 4
        Unavailable: 3, 5, 6, 7, 8, 9, 10, 11
        Not considered: 12

    Args:
        df (pd.DataFrame): Dataframe with total time at each relevant group
            per day and turbine

    Returns:
        pd.DataFrame: Dataframe with extra columns for operation II availability
            info per day and turbine
    """

    # Obtain available time (num)
    df["operation_II_available_time"] = df[1] + df[2] + df[4]

    # Obtain total time (den) (Sum of available and unavailable time)
    df["operation_II_total_time"] = (
        df[1]
        + df[2]
        + df[3]
        + df[4]
        + df[5]
        + df[6]
        + df[7]
        + df[8]
        + df[9]
        + df[10]
        + df[11]
    )

    # Divide
    df["operation_II_availability"] = (
        df["operation_II_available_time"].astype(int) / df["operation_II_total_time"].astype(int) * 100
    ).fillna(0)

    return df
