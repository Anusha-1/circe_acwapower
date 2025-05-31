
from datetime import datetime

import acwa.scripts as s


def main():

    incremental = True # incremental = False if we are adding new columns

    # Load static data (UNCOMMENT TO RELOAD THEM, ONLY IF NECESARY)
    # s.load_10_min_static_data()
    # s.load_alarms_static_data()
    # s.load_1_min_static_data()
    # s.load_pitch_static_data()
    # s.load_met_mast_static_data()
    # s.load_tower_acceleration_static_data()

    # Load static metadata and manufacturer power curves
    # s.upload_alarms_metadata()
    # s.upload_wind_farms()
    # s.upload_turbines()
    # s.upload_densities()
    # s.upload_sectors()
    # s.upload_temperature_signals()
    s.upload_budget_production()
    # s.upload_met_masts()
    # s.upload_variables()

    # Update dynamic mockup
    now = datetime.now()
    s.load_10_min_dynamic_data(now = now)
    s.load_alarms_dynamic_data(now = now)
    s.load_1_min_dynamic_data(now = now)
    s.load_pitch_dynamic_data(now = now)
    s.load_met_mast_dynamic_data(now = now)
    s.load_tower_acceleration_data(now = now)

    # Collect new input data
    s.collect_10_min(incremental = incremental)
    s.collect_alarms(incremental = incremental)
    s.collect_1_min(incremental = incremental)
    s.collect_met_mast(incremental = incremental)

    # Update operational data
    ## Basic Treatment
    s.update_operational_1min_data(incremental = incremental)
    s.update_operational_data_basic(incremental = incremental, year_offset=True)

    ## Power Curves
    s.upload_manufacturer_power_curves() 
    s.generate_power_curves(year_offset=True, plot=True)
    s.interpolate_power_curves()

    ## Reliability
    # s.fit_quantiles(year_offset=True)
    s.predict_quantiles(incremental=incremental)

    ## Advanced Treatment
    s.update_operational_data_losses(incremental = incremental)
    s.update_operational_data_stats()
    s.update_operational_pitch()
    s.calculate_reference_for_pitch()

    # Reliability aggregates 
    s.aggregate_timeseries()
    s.aggregate_for_heatmaps()
    
    # Aggregated measurements
    s.calculate_cumulative_maintenance()
    s.update_availabilities()
    s.allocate_time_and_losses()
    s.calculate_dynamic_yaw()
    s.obtain_max_power_misalignments(year_offset=True)
    s.calculate_performance_ratio(1.12, year_offset=True)
    s.analyze_lapm()
    s.aggregate_tower_acceleration()
    s.calculate_weibull_distributions(year_offset=True)
    
    ## Status
    s.update_status_turbine(year_offset=True)
    s.update_status_met_mast()
    s.update_status_component()

    ## Executive Summary
    s.obtain_executive_summary_kpis()
    s.obtain_executive_summary_alarms()

if __name__ == "__main__":
    main()
