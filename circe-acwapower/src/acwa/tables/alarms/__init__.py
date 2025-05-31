"""
acwa.tables.alarms

Module with schemas for tables containing information on alarms
"""

from .alarms_with_losses import AlarmsLossesSchema
from .basic_alarms import BasicAlarmsSchema
from .input_alarms import InputAlarmsSchema
from .treated_events import TreatedEventsSchema

__all__ = [
    AlarmsLossesSchema, 
    BasicAlarmsSchema, 
    InputAlarmsSchema, 
    TreatedEventsSchema]
