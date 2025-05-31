"""
acwa.alarms

Module to treat alarms

NOTE: Consider to translate these processes to WOD
"""

## Aggregate of alarms
from .aggregate import (
    aggregate_alarms_per_day,
    aggregate_component_per_day,
    aggregate_manufacturer_per_day
)

## Availability calculations
from .availability import (
    obtain_production_based_availabilities,
    obtain_time_based_availabilities, 
    calculate_secs_with_wind_per_day
)

## Custom alarms
from .custom import extract_all_custom_alarms

## Join min data with alarms
from .join import (
    join_alarms_and_10min_data,
    join_alarms_and_1min_data
)

## Alarms metadata
from .metadata import NONREGISTERED_METADATA, UNDERPERFORMING_METADATA

## Priority alarms
from .priority import obtain_priority_alarms, avoid_overlapping_alarms

## Status
from .realtime_status import assign_status

## Stats (MTTR and MTBF)
from .stats import calculate_alarm_stats, get_turbine_stats

__all__ = [

    aggregate_alarms_per_day,
    aggregate_component_per_day,
    aggregate_manufacturer_per_day,
    
    obtain_production_based_availabilities,
    obtain_time_based_availabilities,
    calculate_secs_with_wind_per_day,

    extract_all_custom_alarms,

    join_alarms_and_10min_data,
    join_alarms_and_1min_data,

    NONREGISTERED_METADATA,
    UNDERPERFORMING_METADATA,

    obtain_priority_alarms,
    avoid_overlapping_alarms,
    
    assign_status,
    
    calculate_alarm_stats,
    get_turbine_stats,  
]
