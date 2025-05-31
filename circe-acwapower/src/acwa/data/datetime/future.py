"""
acwa.data.datetime.future

Module to manage future datetimes
"""

from datetime import datetime
import pytz

import pandas as pd

def correct_future_times(
        df: pd.DataFrame,
        cols: list[str],
        ref_datetime: datetime | None = None,
        tz: pytz.BaseTzInfo | None = None
) -> pd.DataFrame:
    """
    Correct one or several columns of datetime object so we can't have future 
    times

    Args:
        df (pd.DataFrame): Dataframe
        cols (list[str]): List of columns to analyze. Should have datetime types
        ref_datetime (datetime | None, optional): Datetime of reference.
            If None, will take datetime.now(). Defaults to None.
        tz (pytz.BaseTzInfo | None, optional): Timezone object. Defaults to None.

    Returns:
        pd.DataFrame: Dataframe with corrected times
    """
    
    if tz is None:
        if ref_datetime is None:
            ref_datetime = datetime.now()
        for col in cols:
            df[col] = df[col].apply(
                lambda x: x if x < ref_datetime else None
            )
    else:
        if ref_datetime is None:
            ref_datetime = datetime.now(tz=pytz.timezone('UTC'))
        for col in cols:
            df[col] = df[col].apply(
                lambda x: x if tz.localize(x) < ref_datetime else None
            )

    return df
