"""
acwa.alarms.aggregate

Module to aggregate alarms (duration and time) accross different categories
(i.e. codes of the alarms, manufacturer concepts or components)
"""

from .code import aggregate_alarms_per_day
from .component import aggregate_component_per_day
from .manufacturer import aggregate_manufacturer_per_day

__all__ = [
    aggregate_alarms_per_day,
    aggregate_component_per_day,
    aggregate_manufacturer_per_day
]