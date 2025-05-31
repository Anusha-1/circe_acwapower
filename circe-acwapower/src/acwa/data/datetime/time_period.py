"""
acwa.data.datetime.time_period

Module to mark higher time periods
"""

from datetime import datetime, timedelta

def obtain_aggregated_time_period(x: datetime, period: str) -> datetime:
    """
    Given a datetime, return a datetime that represents a "higher" level (i.e.
    hour or day)

    Args:
        x (datetime): Datetime to categorize
        period (str): Label of time period to aggregate ("hour" or "day")

    Returns:
        datetime: Higher level datetime
    """

    x_corr = x - timedelta(seconds=1)

    ## Add argument for day or hour
    if period == 'day':
        x_agg = datetime(
            year=x_corr.year, 
            month=x_corr.month,
            day=x_corr.day)
    elif period == 'hour':
        x_agg = datetime(
            year=x_corr.year, 
            month=x_corr.month,
            day=x_corr.day,
            hour=x_corr.hour)

    return x_agg
