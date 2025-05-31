
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pytz

def define_time_limits(now: datetime, min_timestamp: datetime) -> list[dict]:
    """
    Define the time limits for the calculation of power curves

    Args:
        now (datetime): Datetime to consider as the current moment
        min_timestamp (datetime): Minimum timestamp in data

    Returns:
        list[dict]: List of dictionaries, each one defining the needed arguments
            to generate a power curve: start, end, name and short
    """

    utc = pytz.timezone('UTC')
    current_year = now.year
    current_month = now.month

    time_limits = [
        {
            "start": now - timedelta(days=180),
            "end": now - timedelta(days=0),
            "concept": "Historical",
            "period": "6 months",
            "short": "H6",
        },  # Historical
        {
            "start": now - timedelta(days=360),
            "end": now - timedelta(days=0),
            "concept": "Historical",
            "period": "12 months",
            "short": "H12",
        },  # Historical
        {
            "start": now - timedelta(days=60),
            "end": now,
            "concept": "Recent",
            "period": "60 days",
            "short": "R60",
        },  # Recent
        {
            "start": datetime(current_year, 1, 1, 0, 0, 0, tzinfo=utc),
            "end": now,
            "concept": "Recent",
            "period": "YTD",
            "short": "RY"
        },  # YTD
        {
            "start": datetime(current_year, current_month, 1, 0, 0, 0, tzinfo=utc),
            "end": now,
            "concept": "Recent",
            "period": "MTD",
            "short": "RM"
        },  # MTD
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
