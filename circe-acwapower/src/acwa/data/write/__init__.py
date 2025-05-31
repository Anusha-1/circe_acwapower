"""
acwa.data.write

Module to write processed data into the database
"""

from .basic_10min_with_alarms import write_basic_10min
from .manufacturer_availabilities_1day import write_manufacturer_availabilities_1day
from .oper_1day import write_oper_1day
from .oper_10min import write_oper_10min
from .treated_events import write_treated_events
from .treated_events_1day import write_treated_events_1day
from .power_curves import write_power_curves
from .power_curves_metadata import write_power_curves_metadata
from .interpolated_power_curves import write_interpolated_power_curves
from .priority_alarms import write_priority_alarms
from .alarms_with_losses import write_alarms_with_losses
from .wind_speed_corrections import write_wind_speed_corrections
from .component_availabilities_1day import write_component_availabilities_1day
from .oper_1min import write_oper_1min
from .variables import write_variables_table
from .reliability import write_reliability_ts

__all__ = [
    write_basic_10min,
    write_manufacturer_availabilities_1day,
    write_oper_1day, 
    write_treated_events_1day,
    write_treated_events, 
    write_oper_10min,
    write_power_curves,
    write_power_curves_metadata,
    write_interpolated_power_curves,
    write_priority_alarms,
    write_alarms_with_losses,
    write_wind_speed_corrections,
    write_component_availabilities_1day,
    write_oper_1min,
    write_variables_table,
    write_reliability_ts
]
