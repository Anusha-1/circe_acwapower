"""
acwa.scripts.dynamic_load

Scripts to dynamically load raw data as a mockup generator
"""

from .alarms import main as load_alarms_dynamic_data
from .met_mast import main as load_met_mast_dynamic_data
from .min_1 import main as load_1_min_dynamic_data
from .min_10 import main as load_10_min_dynamic_data
from .pitch import main as load_pitch_dynamic_data
from .tower_acceleration import main as load_tower_acceleration_data

__all__ = [
    load_1_min_dynamic_data,
    load_10_min_dynamic_data,
    load_alarms_dynamic_data,
    load_met_mast_dynamic_data,
    load_pitch_dynamic_data,
    load_tower_acceleration_data
]