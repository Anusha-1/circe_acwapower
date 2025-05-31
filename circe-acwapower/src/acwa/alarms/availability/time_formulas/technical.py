"""
acwa.alarms.availability.time_formulas.technical

Formula for technical availability
"""

import pandas as pd

def apply_technical_availability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the technical availability formula:

        technical_availability = 1 - Unavail Time / (Avail Time + Unavail Time)

    where Available and Unavailable Time come from the following priority groups:

        Available: 1 to 6
        Unavailable: 8, 9
        Not considered: 7, 10, 11, 12

    Args:
        df (pd.DataFrame): Dataframe with total time at each relevant group
            per day and turbine

    Returns:
        pd.DataFrame: Dataframe with extra columns for technical availability
            info per day and turbine
    """

    # Obtain available time (num)
    df["technical_available_time"] = (
        df[1] + df[2] + df[3] + df[4] + df[5] + df[6]
    )

    # Obtain total time (den) (Sum of available and unavailable time)
    df["technical_total_time"] = (
        df[1]
        + df[2]
        + df[3]
        + df[4]
        + df[5]
        + df[6]
        + df[8]
        + df[9]
    )

    # Divide
    df["technical_availability"] = (
        df["technical_available_time"].astype(int) / df["technical_total_time"].astype(int) * 100
    ).fillna(0)

    return df