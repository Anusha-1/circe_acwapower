"""
acwa.alarms.availability.time_formulas.contractual

Formula for contractual availability
"""

import pandas as pd

def apply_contractual_availability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the contractual availability formula (Khalladi):

        contractual_availability = Period Time - Failure Time + Maintenance / Period Time

    where these groups correspond to the following priority values:

        Period Time: All except 12
        Failure Time: 8, 9, 10
        Maintenance: 7

    PENDING TASKS:
        - Maintenance only up to 80 hours/year, from that point it shoud be
            count as Failure. We should not need to change anything here though,
            when a maintenance alarm surpasses the threshold, we should change
            its priority.
        - This is exclusive for Khalladi, in other cases we should have a
            different calculation

    Args:
        df (pd.DataFrame): Dataframe with total time at each relevant group
            per day and turbine

    Returns:
        pd.DataFrame: Dataframe with extra columns for contractual availability
            info per day and turbine
    """

    # Obtain the groups
    period_time = (
        df["1_contractual"]
        + df["2_contractual"]
        + df["3_contractual"]
        + df["4_contractual"]
        + df["5_contractual"]
        + df["6_contractual"]
        + df["7_contractual"]
        + df["8_contractual"]
        + df["9_contractual"]
        + df["10_contractual"]
        + df["11_contractual"]
    )
    failure_time = df["8_contractual"] + df["9_contractual"] + df["10_contractual"]
    maintenance = df["7_contractual"]

    # Obtain available time (num)
    df["contractual_available_time"] = (
        period_time - failure_time + maintenance
    )

    # Obtain total time (den) (Sum of available and unavailable time)
    df["contractual_total_time"] = period_time

    # Divide
    df["contractual_availability"] = (
        df["contractual_available_time"].astype(int) / df["contractual_total_time"].astype(int) * 100
    ).fillna(0)

    # Apply correction
    df['contractual_availability'] = df['contractual_availability'].apply(
        lambda x: min(x, 100.0))

    return df