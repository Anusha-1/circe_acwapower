"""
acwa.data.datetime

Module with auxiliary functions to manage datetime objects
"""

from .col_to_datetime import transform_to_datetime
from .duration import add_duration
from .extend_days import extend_by_days
from .format import format_timedelta_to_HHMMSS
from .future import correct_future_times
from .maintenance_limits import generate_maintenance_time_limits
from .time_period import obtain_aggregated_time_period
from .timezone import transform_timezone
from .year import change_year

__all__ = [
    transform_to_datetime,
    add_duration,
    extend_by_days,
    format_timedelta_to_HHMMSS,
    correct_future_times,
    transform_timezone,
    change_year,
    obtain_aggregated_time_period,
    generate_maintenance_time_limits
]