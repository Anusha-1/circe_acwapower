"""
acwa.yaw.max_power.time_limits

Define the time limits for max power misallignment calculations
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
from typing import Any

def define_max_power_misallignement_time_limits(
        year_offset: bool = False) -> list[dict[str, Any]]:
    """
    Return the time limits to use in max power misallignments calculation

    Args:
        year_offset (bool, optional): If True, move the present to 2023 to work
            with a mockup od 2023 data. Defaults to False

    Returns:
        list[dict[str, Any]]: List of dictionaries, each one delimiting the 
            period for a max power calculation. Each one has the following keys:

            - 'start'
            - 'end'
            - 'period'
    """

    utc = pytz.timezone('UTC')
    now = datetime.now(tz=utc) - year_offset*relativedelta(year=2023)

    return [
        {
            'start': datetime(now.year, 1, 1, 0, 0, 0, tzinfo=utc),
            'end': now,
            'period': 'This year'
        },
        {
            'start': now - timedelta(days=60),
            'end': now,
            'period': 'last 60 days'
        }
    ]
