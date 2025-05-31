"""
acwa.tables.aggregation

Collection of schemas for aggregated tables
"""

from .component_availabilities_1day import ComponentAvailabilities1DaySchema
from .dynamic_yaw import DynamicYawSchema
from .lapm_analysis import LapmAnalysisSchema
from .manufacturer_availabilities_1day import ManufacturerAvailabilities1DaySchema
from .max_power_misallignment import MaxPowerMisallignmentSchema
from .oper_1day import Oper1DaySchema
from .performance_ratio import PerformanceRatioSchema
from .tower_acceleration import TowerAcceleration1DaySchema
from .treated_events_1day import TreatedEvents1DaySchema

__all__ = [
    ComponentAvailabilities1DaySchema,
    DynamicYawSchema,
    LapmAnalysisSchema,
    ManufacturerAvailabilities1DaySchema,
    MaxPowerMisallignmentSchema,
    Oper1DaySchema,
    PerformanceRatioSchema,
    TowerAcceleration1DaySchema,
    TreatedEvents1DaySchema
    ]
