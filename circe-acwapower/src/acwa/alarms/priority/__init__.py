"""
acwa.alarms.priority

Module to establish non-overlapping priority alarms 
"""

from .main import obtain_priority_alarms, avoid_overlapping_alarms

__all__ = [obtain_priority_alarms, avoid_overlapping_alarms]
