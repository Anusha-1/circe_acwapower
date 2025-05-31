"""
acwa.alarms.availability.time_formulas.operation_I

Formula for operation availability option I
"""

import pandas as pd


def apply_operation_I_availability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the operation I availability formula:

        operation_I_availability = 1 - Unavail Time / (Avail Time + Unavail Time)

    where Available and Unavailable Time come from the following priority groups:

        Available: 1 and 2
        Unavailable: 3 to 11
        Not considered: 12

    Args:
        df (pd.DataFrame): Dataframe with total time at each relevant group
            per day and turbine

    Returns:
        pd.DataFrame: Dataframe with extra columns for operation I availability
            info per day and turbine
    """

    # Obtain available time (num)
    df["operation_I_available_time"] = (df[1] + df[2])

    # Obtain total time (den) (Sum of available and unavailable time)
    df["operation_I_total_time"] = (
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
    df["operation_I_availability"] = (
        df["operation_I_available_time"].astype(int) / df["operation_I_total_time"].astype(int) * 100
    ).fillna(0)

    return df
