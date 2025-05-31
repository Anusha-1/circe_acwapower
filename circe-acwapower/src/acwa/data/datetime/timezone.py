"""
acwa.data.datetime.timezone

Module to transform between timezones
"""

import pytz

import pandas as pd

def transform_timezone(
        df: pd.DataFrame,
        time_col: str,
        orig_tz: pytz.BaseTzInfo,
        dest_tz: pytz.BaseTzInfo,
        dest_col: str | None = None
) -> pd.DataFrame:
    """
    Transform a column of datetime values from one timezone to another

    Args:
        df (pd.DataFrame): Dataframe
        time_col (str): Datetime column to transform
        orig_tz (pytz.BaseTzInfo): Timezone of origin data
        dest_tz (pytz.BaseTzInfo): Timezone to transform to
        dest_col (str | None, optional): Name of column to save the transformed 
            values. If None, it replaces the original column. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe with column with transformed datetime objects
    """
    
    if dest_col is None:
        dest_col = time_col

    df[dest_col] = df[time_col].apply(
        lambda x: orig_tz.localize(x).astimezone(dest_tz) if not pd.isnull(x) else x
    )

    return df
