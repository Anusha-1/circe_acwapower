"""
acwa.data.compilation.mapping.min_10

Mapping functions for 10-min signals
"""

from .khalladi import map_10min_Khalladi
from .khalladi_pitch import map_10min_pitch_Khalladi
from .khalladi_tower_acc import map_10min_tower_acc_Khalladi


DICT_MAP_10MIN = {
    'realtime_input_10min_Khalladi': map_10min_Khalladi,
    'realtime_input_10min_Azerbaijan': map_10min_Khalladi,
    'realtime_tower_acceleration_Khalladi': map_10min_tower_acc_Khalladi,
    'realtime_tower_acceleration_Azerbaijan': map_10min_tower_acc_Khalladi,
    'realtime_pitch_Khalladi': map_10min_pitch_Khalladi,
    'realtime_pitch_Azerbaijan': map_10min_pitch_Khalladi,
}

__all__ = [DICT_MAP_10MIN]
