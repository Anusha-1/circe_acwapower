"""
acwa.scripts.power_curves

Scripts related with the generation of power curves
"""

from .data import main as generate_power_curves
from .interpolation import main as interpolate_power_curves
from .manufacturer import main as upload_manufacturer_power_curves

__all__ = [
    generate_power_curves,
    interpolate_power_curves,    
    upload_manufacturer_power_curves
    ]

