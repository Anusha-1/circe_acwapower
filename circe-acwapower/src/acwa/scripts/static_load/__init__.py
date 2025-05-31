"""
acwa.scripts.static_load

Scripts to load static files into DB tables
"""

from .alarms import main as load_alarms_static_data
from .met_mast import main as load_met_mast_static_data
from .min_1 import main as load_1_min_static_data
from .min_10 import main as load_10_min_static_data
from .pitch import main as load_pitch_static_data
from .tower_acceleration import main as load_tower_acceleration_static_data

__all__ = [
    load_1_min_static_data,
    load_10_min_static_data,
    load_alarms_static_data,
    load_met_mast_static_data,    
    load_pitch_static_data,
    load_tower_acceleration_static_data
]
