"""
acwa.data.format.tower_xy

Module to melt tower acceleration data
"""

import pandas as pd


def melt_tower_xy_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melt tower acceleration data

    Args:
        df (pd.DataFrame): Dataframe from input_10min

    Returns:
        pd.DataFrame: Dataframe in new format (statistic and direction as columns)
    """

    df = pd.melt(
        df,
        id_vars=[
            "id_wf",
            "id_wtg",
            "id_wtg_complete",
            "timestamp"
        ],
        var_name="variable",
        value_name="value",
    )

    df["statistic"] = df["variable"].apply(lambda x: x[21:24])
    df["direction"] = df["variable"].apply(lambda x: x[9].upper())

    df = df.drop(columns=["variable"])

    return df
