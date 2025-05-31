"""
acwa.data.datetime.col_to_datetime

Module to transform pandas columns to datetime
"""

import pandas as pd

from acwa.data.datetime.year import change_year

def transform_to_datetime(
        df: pd.DataFrame,
        original_col: str,
        format: str,
        dest_col: str = 'datetime',
        new_year: int = None,
        drop_original_col: bool = True
) -> pd.DataFrame:
    """
    Trasnform a column with string timstamp into a column with datetime objets

    Args:
        df (pd.DataFrame): DataFrame
        original_col (str): Original column containing the timestamps as strings
        format (str): Format of the timestamps
        dest_col (str, optional): Destination column name. 
            Defaults to 'datetime'.
        new_year (int, optional): If a year is passed, we change the year of the
            datetimes, useful for mocking real-time with historic data. 
            Defaults to None.
        drop_original_col (bool, optional): If True, drops the original columns.
            Defaults to True.

    Returns:
        pd.DataFrame: Dataframe after transformation
    """
    
    ## Transform the dates       
    df[dest_col] = pd.to_datetime(
        df[original_col], 
        format=format)
    
    if new_year is not None:
        df = change_year(df, dest_col, new_year)

    if drop_original_col:
        df = df.drop(columns=original_col)

    return df