"""
acwa.data.compilation.mapping

Module with the mapping functions for each Wind Farm and table
"""

from .alarms import DICT_MAP_ALARMS
from .met_mast import DICT_MAP_MM
from .min_10 import DICT_MAP_10MIN
from .min_1 import DICT_MAP_1MIN

__all__ = [DICT_MAP_10MIN, DICT_MAP_1MIN, DICT_MAP_MM, DICT_MAP_ALARMS]
