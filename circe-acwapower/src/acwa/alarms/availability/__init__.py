"""
acwa.alarms.availability

Module with calculations related to availability
"""

from .production import obtain_production_based_availabilities
from .time import obtain_time_based_availabilities
from .wind import calculate_secs_with_wind_per_day

__all__ = [
    obtain_production_based_availabilities,
    obtain_time_based_availabilities,   
    calculate_secs_with_wind_per_day
]