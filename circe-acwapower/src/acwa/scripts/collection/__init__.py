"""
acwa.scripts.collection

Scripts to collect and standarize dynamic data
"""

from .alarms import main as collect_alarms
from .min_1 import main as collect_1_min
from .min_10 import main as collect_10_min
from .met_mast import main as collect_met_mast

__all__ = [
    collect_alarms,
    collect_1_min,
    collect_10_min,
    collect_met_mast
]
