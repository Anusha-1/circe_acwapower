"""
acwa.data.compilation

Module with functions for data compilation process
"""

from .replace_flag import obtain_replace_flag
from .max_datetime import extract_maximum_datetime
from .raw_table import extract_raw_data
from .missing import complete_missing_signals
from .load_info import load_mapping_information

from .mapping import DICT_MAP_10MIN, DICT_MAP_1MIN, DICT_MAP_MM, DICT_MAP_ALARMS

from .append_alarms import append_new_alarms
from .update_alarms import update_input_alarms

__all__ = [
    append_new_alarms,
    update_input_alarms,

    obtain_replace_flag,
    extract_maximum_datetime,
    extract_raw_data,
    complete_missing_signals,
    load_mapping_information,
    DICT_MAP_10MIN, 
    DICT_MAP_1MIN,
    DICT_MAP_MM,
    DICT_MAP_ALARMS
]
