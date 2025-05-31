"""
acwa.alarms.stats

Module to calculate stats regarding the duration of the alarms (MTTR, MTBF)
"""

from .past_all import calculate_alarm_stats
from .mttr_mtbf import get_turbine_stats

__all__ = [calculate_alarm_stats, get_turbine_stats]
