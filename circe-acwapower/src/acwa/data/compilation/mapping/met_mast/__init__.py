"""
acwa.data.compilation.mapping.met_mast

Mapping functions for met mast signals
"""

from .khalladi import map_met_mast_Khalladi

DICT_MAP_MM = {
    "realtime_met_mast_Kh-M1": map_met_mast_Khalladi,
    "realtime_met_mast_Az-M1": map_met_mast_Khalladi
}

__all__ = [DICT_MAP_MM]
