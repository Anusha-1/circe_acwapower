"""
acwa.alarms.join

Module to manage the join of minutal data and alarms
"""

from .min_10 import join_alarms_and_10min_data
from .min_1 import join_alarms_and_1min_data

__all__ = [join_alarms_and_10min_data, join_alarms_and_1min_data]
