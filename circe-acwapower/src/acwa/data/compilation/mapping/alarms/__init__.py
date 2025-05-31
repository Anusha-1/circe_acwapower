"""
acwa.data.compilation.mapping.alarms

Mapping functions for alarms
"""

from .khalladi import map_alarms_Khalladi

DICT_MAP_ALARMS = {
    'Khalladi': map_alarms_Khalladi,
    'Azerbaijan': map_alarms_Khalladi
}

__all__ = [DICT_MAP_ALARMS]
