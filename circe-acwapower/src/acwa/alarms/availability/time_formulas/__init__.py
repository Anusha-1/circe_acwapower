"""
acwa.alarms.availability.formulas

Module with availability formulas to apply over dataframe
"""

from .wind import apply_wind_availability

# Norm availabilities
from .operation_I import apply_operation_I_availability
from .operation_II import apply_operation_II_availability
from .operation_III import apply_operation_III_availability
from .technical import apply_technical_availability
from .contractual import apply_contractual_availability

__all__ = [
    apply_technical_availability,
    apply_contractual_availability,
    apply_wind_availability,
    apply_operation_I_availability,
    apply_operation_II_availability,
    apply_operation_III_availability
    ]