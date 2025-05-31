"""
acwa.lapm

Module with auxiliary functions for lapm analysis
"""

from .all import apply_lapm_identification_at_all_turbines
from .dispersion import calculate_dispersion

__all__ = [calculate_dispersion, apply_lapm_identification_at_all_turbines]
