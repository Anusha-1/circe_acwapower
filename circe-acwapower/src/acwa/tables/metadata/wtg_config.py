"""
acwa.tables.wtg_config

Validation schema for wtg_config table
"""

from datetime import date
import pandera as pa
from pandera.typing import Series

class WtgConfigSchema(pa.DataFrameModel):
    """Schema for table wtg_config table"""

    id_wf: Series[str] = pa.Field() # Wind Farm
    wf_name: Series[str] = pa.Field() # wf name
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field(unique=True) # Complete turbine id 
    wtg_name: Series[str] = pa.Field() # Turbine name

    latitude: Series[float] = pa.Field(ge=-90, le=90) # Latitude
    longitude: Series[float] = pa.Field(ge=-180, le=180) # Longitude
    elevation: Series[int] = pa.Field() #turbine elevation
    contractual_date: Series[date]
    nominal_power: Series[int] = pa.Field(ge=0) # Nominal power (kW)
    rotor_diameter: Series[int] = pa.Field(ge=0) # Rotor diameter (m)
    model: Series[str] = pa.Field() # Model of turbine
    manufacturer: Series[str] = pa.Field() # Manufacturer 
    wind_speed_start: Series[float] = pa.Field(ge=0) # m/s
    wind_speed_stop: Series[float] = pa.Field(ge=0) # m/s
    reference_pc: Series[str] = pa.Field() 
 
    group: Series[str] = pa.Field()
    id_group_complete: Series[str] = pa.Field()
    met_mast_id: Series[str] = pa.Field()
    LT_wtg: Series[float] = pa.Field()
    contractual_limit: Series[int]  = pa.Field(ge=0, le=100) # Maybe it should be float
