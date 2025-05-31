"""
acwa.scripts.metadata

Collection of sctipts to upload metadata information
"""

from .alarms import main as upload_alarms_metadata
from .budget_production import main as upload_budget_production
from .densities import main as upload_densities
from .sectors import main as upload_sectors
from .temperature_signals import main as upload_temperature_signals
from .turbines import main as upload_turbines
from .variables_and_mapping import main as upload_variables_and_mapping
from .wind_farms import main as upload_wind_farms
from .met_mast import main as upload_met_masts

def upload_all_metadata():
    """Runs all the script to upload metadata"""
    upload_alarms_metadata()
    upload_budget_production()
    upload_wind_farms()
    upload_turbines()
    upload_temperature_signals()
    upload_densities()
    upload_variables_and_mapping()
    upload_sectors()
    upload_met_masts()
    
__all__ = [
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
]