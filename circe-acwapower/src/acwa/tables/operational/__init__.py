"""
acwa.tables.operational

Module with the Schemas for the operational tables (10-min and 1-min)
"""

from .basic_10min import Basic10minSchema
from .input_1min import Input1minSchema
from .input_10min import Input10minSchema
from .maintenance import MaintenanceSchema
from .met_mast import MetMastSchema
from .oper_1min import Oper1minSchema
from .oper_10min import Oper10minSchema
from .wind_speed_corrections import WindSpeedCorrectionsSchema

__all__ = [
    Basic10minSchema,
    Input1minSchema,
    Input10minSchema,
    Oper1minSchema,
    Oper10minSchema,
    MaintenanceSchema,
    MetMastSchema,
    WindSpeedCorrectionsSchema
    ]
