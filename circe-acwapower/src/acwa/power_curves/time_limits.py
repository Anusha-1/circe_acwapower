"""
acwa.power_curves.time_limits

Module to define the time periods for the calculated power curves
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

def define_time_limits(now: datetime, min_timestamp: datetime) -> list[dict]:
    """
    Define the time limits for the calculation of power curves

    Args:
        now (datetime): Datetime to consider as the current moment

    Returns:
        list[dict]: List of dictionaries, each one defining the needed arguments
            to generate a power curve: start, end, name and short
    """

    current_year = now.year
    current_month = now.month
    utc = pytz.timezone('UTC')

    time_limits = [
        {
            "start": now - timedelta(days=240),
            "end": now - timedelta(days=60),
            "concept": "Historical",
            "period": "6 months",
            "short": "H6",
        },  # Historical
        {
            "start": now - timedelta(days=420),
            "end": now - timedelta(days=60),
            "concept": "Historical",
            "period": "12 months",
            "short": "H12",
        },  # Historical
        {
            "start": datetime(current_year - 1, 1, 1, tzinfo=utc),
            "end": datetime(current_year, 1, 1, tzinfo=utc),
            "concept": "Historical",
            "period": "previous year",
            "short": "HPY",
        },  # Historical
        {
            "start": now - timedelta(days=60),
            "end": None,
            "concept": "Rolling",
            "period": "60 days",
            "short": "R60",
        },  # Rolling
        {
            "start": now - timedelta(days=30),
            "end": None,
            "concept": "Rolling",
            "period": "30 days",
            "short": "R30",
        },  # Rolling
        {
            "start": now - timedelta(days=15),
            "end": None,
            "concept": "Rolling",
            "period": "15 days",
            "short": "R15",
        },  # Rolling
    ]

    ## Months in data
    min_year = min_timestamp.year
    min_month = min_timestamp.month
    for year in range(min_year, current_year+1):

        initial_month = min_month if year == min_year else 1
        final_month = current_month if year == current_year else 12
        
        for month in range(initial_month, final_month+1):

            start_date = datetime(year, month, 1, 0, 0, 0, tzinfo=utc)

            time_limits.append(
                {
                    "start": start_date,
                    "end": start_date + relativedelta(months=1),
                    "concept": "Monthly",
                    "period": start_date.strftime("%Y-%B"),
                    "short": start_date.strftime("%Y-%b"),
                }
            )


    return time_limits
