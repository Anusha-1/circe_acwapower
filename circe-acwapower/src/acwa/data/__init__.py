"""
acwa.data

Module for basic data manipulation
"""

from .aggregate import (
    aggregate_values_daily,
    add_daily_budget,
    aggregate_values_from_1min
    )

from .calc import (
    calculate_density_10min, 
    correct_speed_with_density,
    create_lapm_sectors_dataframe,
    obtain_main_direction,
    obtain_distribution_of_directions,
    obtain_main_sectors,
    check_sectors_overlap,
    obtain_all_sectors,
    assign_sector_10min,
    classify_in_bin,
    correct_speed_with_density_auto
    )

from .check_incremental import (
    check_incremental_flag, 
    check_incremental_flag_basic,
    check_incremental_flag_1min,
    check_incremental_flag_pitch
)

from .compilation import (
    update_input_alarms,
    append_new_alarms,
    obtain_replace_flag,
    extract_maximum_datetime,
    extract_raw_data,    
    complete_missing_signals,
    load_mapping_information,
    DICT_MAP_10MIN,
    DICT_MAP_1MIN,
    DICT_MAP_MM,
    DICT_MAP_ALARMS
)

from .datetime import (
    change_year, 
    transform_to_datetime,
    extend_by_days,
    correct_future_times,
    add_duration,
    transform_timezone,
    obtain_aggregated_time_period,
    generate_maintenance_time_limits
    )

from .densities import correct_by_densities

from .format import melt_pitch_data, melt_tower_xy_data

from .horizon import (
    extract_alarms_temporal_horizon, 
    extract_alarms_temporal_horizon_basic
)

from .merged import obtain_reliability_input

from .missing import fill_gaps

from .ml_format import (
    format_features_for_reliability, 
    split_Xy_for_reliability
)

from .read import (
    read_basic_10min_data, 
    read_input_10min_data, 
    read_basic_alarms,
    read_input_1min_data,
    read_input_pitch_data,
    read_input_tower_xy_data
    )

from .summary import (
    sum_kpis_at_wind_farm, 
    add_performance_ratio_to_kpis,
    add_overtemperature_to_kpis,
    extract_summary_alarms
    )

from .time_aggregation import aggregate_by_classification_labels

from .weibull import define_time_limits

from .write import (
    write_treated_events, 
    write_oper_10min, 
    write_oper_1day,
    write_treated_events_1day,
    write_basic_10min,
    write_power_curves,
    write_power_curves_metadata,
    write_manufacturer_availabilities_1day,
    write_interpolated_power_curves,
    write_priority_alarms,
    write_alarms_with_losses,
    write_wind_speed_corrections,
    write_component_availabilities_1day,
    write_oper_1min,
    write_variables_table, ## Soon to be deprecated ?
    write_reliability_ts
    )

__all__ = [

    ## Aggregate
    aggregate_values_daily,
    add_daily_budget,
    aggregate_values_from_1min,

    ## Calc
    calculate_density_10min, 
    correct_speed_with_density,
    create_lapm_sectors_dataframe,
    obtain_main_direction,
    obtain_distribution_of_directions,
    obtain_main_sectors,
    check_sectors_overlap,
    obtain_all_sectors,
    assign_sector_10min,
    classify_in_bin,
    correct_speed_with_density_auto,
    
    ## Check incremental
    check_incremental_flag, 
    check_incremental_flag_basic,
    check_incremental_flag_1min,
    check_incremental_flag_pitch,

    ## Compilation
    update_input_alarms,
    append_new_alarms,
    obtain_replace_flag,
    extract_maximum_datetime,
    extract_raw_data,    
    complete_missing_signals,
    load_mapping_information,
    DICT_MAP_10MIN,
    DICT_MAP_1MIN,
    DICT_MAP_MM,
    DICT_MAP_ALARMS,

    ## Datetime
    change_year, 
    transform_to_datetime,
    correct_future_times,
    add_duration,
    transform_timezone,
    obtain_aggregated_time_period,
    generate_maintenance_time_limits,
    extend_by_days,

    ## Densities
    correct_by_densities,

    ## Format
    melt_pitch_data,
    melt_tower_xy_data,

    ## Horizon
    extract_alarms_temporal_horizon, 
    extract_alarms_temporal_horizon_basic,

    ## Merged
    obtain_reliability_input,

    ## Missing
    fill_gaps,

    ## ML format
    format_features_for_reliability, 
    split_Xy_for_reliability,

    ## Read
    read_basic_10min_data, 
    read_input_10min_data, 
    read_basic_alarms,
    read_input_1min_data,
    read_input_pitch_data,
    read_input_tower_xy_data,

    ## Summary
    sum_kpis_at_wind_farm, 
    add_performance_ratio_to_kpis,
    add_overtemperature_to_kpis,
    extract_summary_alarms,

    ## Time aggregation
    aggregate_by_classification_labels,

    ## Weibull
    define_time_limits,

    ## Write
    write_treated_events, 
    write_oper_10min, 
    write_oper_1day,
    write_treated_events_1day,
    write_basic_10min,
    write_power_curves,
    write_power_curves_metadata,
    write_manufacturer_availabilities_1day,
    write_interpolated_power_curves,
    write_priority_alarms,
    write_alarms_with_losses,
    write_wind_speed_corrections,
    write_component_availabilities_1day,
    write_oper_1min,
    write_variables_table,
    write_reliability_ts,
]
