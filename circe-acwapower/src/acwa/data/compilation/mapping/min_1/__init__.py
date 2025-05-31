"""
acwa.data.compilation.mapping.min_10

Mapping functions for 10-min signals
"""

from ..min_10.khalladi import map_10min_Khalladi

DICT_MAP_1MIN = {
    'realtime_input_1min_Khalladi': map_10min_Khalladi,
    'realtime_input_1min_Azerbaijan': map_10min_Khalladi
}

__all__ = [DICT_MAP_1MIN]
