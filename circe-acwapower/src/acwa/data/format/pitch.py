"""
acwa.data.format.pitch

Module to melt pitch data
"""

import pandas as pd


def melt_pitch_data(df: pd.DataFrame, pitch_limit: int = 20) -> pd.DataFrame:
    """
    Melt pitch data

    Args:
        df (pd.DataFrame): Dataframe from input_10min
        pitch_limit (int, optional). Pitch Limit to consider. Defaults to 20

    Returns:
        pd.DataFrame: Dataframe in new format (statistic and blade as columns)
    """

    df = pd.melt(
        df,
        id_vars=[
            "id_wf",
            "id_wtg",
            "id_wtg_complete",
            "timestamp",
            "lambda_parameter",
        ],
        var_name="variable",
        value_name="pitch_angle",
    )

    df["statistic"] = df["variable"].apply(lambda x: x[-3:])
    df["blade"] = df["variable"].apply(lambda x: x[10].upper())

    df = df.drop(columns=["variable"])

    ## Limit to pitch threshold
    df["value_limited"] = df["pitch_angle"].apply(lambda x: min(x, pitch_limit))
    df["limited"] = df["pitch_angle"] != df["value_limited"]
    df["pitch_angle"] = df["value_limited"]
    df = df.drop(columns=["value_limited"])

    return df
