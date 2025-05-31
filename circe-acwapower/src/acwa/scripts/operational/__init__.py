"""
acwa.scripts.operational

Module to analyze data in real-time
"""

from .basic import main as update_operational_data_basic
from .losses import main as update_operational_data_losses
from .min_1 import main as update_operational_1min_data
from .pitch import main as update_operational_pitch
from .reference import main as calculate_reference_for_pitch
from .stats import main as update_operational_data_stats


__all__ = [
    update_operational_1min_data,
    update_operational_data_basic,
    update_operational_data_losses,
    update_operational_pitch,
    calculate_reference_for_pitch,
    update_operational_data_stats
]