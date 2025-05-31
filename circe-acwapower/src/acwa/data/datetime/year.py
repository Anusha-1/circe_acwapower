"""
acwa.data.datetime.year

Module to modify years
"""

from dateutil.relativedelta import relativedelta

import pandas as pd

def change_year(
        df: pd.DataFrame,
        date_col: str,
        new_year: int
) -> pd.DataFrame:
    """
    Changes the year in a column of datetime

    Args:
        df (pd.DataFrame): DataFrame
        date_col (str): Column containing the datetimes to change 
        new_year (int): New year to input in the data

    Returns:
        pd.DataFrame: Dataframe after transformation
    """

    df[date_col] = df[date_col].apply(
        lambda x: x + relativedelta(year=new_year)
    )

    return df