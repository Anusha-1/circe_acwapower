"""
acwa.scripts

Module with scripts to be place as azure functions
"""

from .metadata import (
    upload_alarms_metadata,
    upload_budget_production,
    upload_wind_farms,
    upload_turbines,
    upload_densities,
    upload_variables_and_mapping,
    upload_sectors,
    upload_temperature_signals,
    upload_met_masts,
    
    upload_all_metadata
)

from .power_curves import (
    upload_manufacturer_power_curves,
    generate_power_curves,
    interpolate_power_curves,
)

from .static_load import(
    load_1_min_static_data,
    load_10_min_static_data,
    load_alarms_static_data,
    load_met_mast_static_data,
    load_pitch_static_data,
    load_tower_acceleration_static_data
)

from .dynamic_load import (
    load_1_min_dynamic_data,
    load_10_min_dynamic_data,
    load_alarms_dynamic_data,
    load_met_mast_dynamic_data,
    load_pitch_dynamic_data,
    load_tower_acceleration_data
)

from .collection import (
    collect_alarms,
    collect_1_min,
    collect_10_min,
    collect_met_mast,
)

from .operational import (
    update_operational_1min_data,
    update_operational_data_basic,
    update_operational_data_losses,
    update_operational_pitch,
    calculate_reference_for_pitch,
    update_operational_data_stats
)

from .status import (
    update_status_turbine,
    update_status_met_mast,
    update_status_component
)

from .reliability import (
    fit_quantiles,
    predict_quantiles,
    aggregate_timeseries,
    aggregate_for_heatmaps
)

from .aggregation import (
    aggregate_tower_acceleration,
    calculate_cumulative_maintenance,
    calculate_dynamic_yaw,
    update_availabilities,
    allocate_time_and_losses,
    obtain_max_power_misalignments,
    calculate_performance_ratio,
    analyze_lapm,
    calculate_weibull_distributions
)

from .executive_summary import (
    obtain_executive_summary_kpis,
    obtain_executive_summary_alarms
)

__all__ = [

    ## Metadata scripts
    upload_alarms_metadata,
    upload_wind_farms,
    upload_turbines,
    upload_densities,
    upload_variables_and_mapping,
    upload_sectors,
    upload_temperature_signals,
    upload_met_masts,
    upload_budget_production,
    upload_all_metadata,

    ## Power Curve scripts
    upload_manufacturer_power_curves,
    generate_power_curves,
    interpolate_power_curves,

    ## Static Load scripts
    load_1_min_static_data,
    load_10_min_static_data,
    load_alarms_static_data,
    load_met_mast_static_data,
    load_pitch_static_data,
    load_tower_acceleration_static_data,

    ## Dynamic Load scripts
    load_1_min_dynamic_data,
    load_10_min_dynamic_data,
    load_alarms_dynamic_data,
    load_met_mast_dynamic_data,
    load_pitch_dynamic_data,
    load_tower_acceleration_data,

    ## Collection
    collect_alarms,
    collect_1_min,
    collect_10_min,
    collect_met_mast,

    ## Operational
    update_operational_1min_data,
    update_operational_data_basic,   
    update_operational_data_losses,
    update_operational_pitch,
    calculate_reference_for_pitch,
    update_operational_data_stats,

    ## Status
    update_status_turbine,
    update_status_met_mast,
    update_status_component,

    ## Reliability
    fit_quantiles,
    predict_quantiles,
    aggregate_timeseries,
    aggregate_for_heatmaps,

    ## Aggregation
    aggregate_tower_acceleration,
    calculate_cumulative_maintenance,
    update_availabilities, 
    allocate_time_and_losses,
    calculate_dynamic_yaw,
    obtain_max_power_misalignments,
    calculate_performance_ratio,
    analyze_lapm,
    calculate_weibull_distributions,

    ## Executive Summary
    obtain_executive_summary_kpis,
    obtain_executive_summary_alarms,
        
]
