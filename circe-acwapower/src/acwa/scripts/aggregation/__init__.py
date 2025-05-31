"""
acwa.scripts.aggregation

Module with scripts to aggregate results
"""

from .allocation import main as allocate_time_and_losses
from .availabilities import main as update_availabilities
from .dynamic_yaw import main as calculate_dynamic_yaw
from .lapm_analysis import main as analyze_lapm
from .maintenance import main as calculate_cumulative_maintenance
from .max_power_misalignment import main as obtain_max_power_misalignments
from .performance_ratio import main as calculate_performance_ratio
from .tower_acceleration import main as aggregate_tower_acceleration
from .weibull_calc import main as calculate_weibull_distributions

__all__ = [
    allocate_time_and_losses,
    update_availabilities,
    calculate_dynamic_yaw,
    calculate_cumulative_maintenance,
    obtain_max_power_misalignments,
    aggregate_tower_acceleration,
    calculate_performance_ratio,
    analyze_lapm,
    calculate_weibull_distributions
]
