"""
acwa.tables.wf_config

Validation schema for wf_config table
"""

from datetime import date

import pytz

import pandera as pa
from pandera.typing import Series

class WfConfigSchema(pa.DataFrameModel):
    """Schema for table wf_config table"""

    id_country: Series[int] = pa.Field(lt=1000) # Id country
    id_wf: Series[str] = pa.Field(unique=True) # Wind Farm
    wf_name: Series[str] = pa.Field() # wf name
    latitude: Series[float] = pa.Field(ge=-90, le=90) # Latitude
    longitude: Series[float] = pa.Field(ge=-180, le=180) # Longitude

    number_of_wtg: Series[int] = pa.Field(gt=0) # Number of turbines
    installed_power: Series[float] = pa.Field(ge=0) # Total nominal power (MW)
    contractual: Series[float] = pa.Field(le=100, ge=0) # Contractual availability
    betz_limit: Series[float] = pa.Field() # Betz limit
    tz_data : Series[str] = pa.Field(isin=pytz.all_timezones)
    tz_alarms : Series[str] = pa.Field(isin=pytz.all_timezones)
    pitch_limit: Series[int] = pa.Field() # Limit to filter pitch angle data

    reference_turbine: Series[str] = pa.Field() # Reference turbine id_wtg_complete
    reference_start: Series[date] = pa.Field() # Beginning of reference period
    reference_end: Series[date] = pa.Field() # End of reference period
    
    # Add more ? ...
