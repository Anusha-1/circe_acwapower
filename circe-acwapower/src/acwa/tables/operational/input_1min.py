"""
acwa.tables.basic_input_1min

Validation schema for input_1min table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class Input1minSchema(pa.DataFrameModel):
    """Schema for table input_1min"""

    id_wf: Series[str] = pa.Field() # Wind Farm
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 

    timestamp: Series[datetime] = pa.Field() # Timestamp
    wind_speed: Series[float] = pa.Field(nullable=True) # Wind Speed
    power: Series[float] = pa.Field(nullable=True) # Power
    temperature: Series[float] = pa.Field(nullable=True) # Temperature
    wind_direction: Series[float] = pa.Field(nullable=True) # Wind direction
    rotor_rpm: Series[float] =pa.Field(nullable=True) # Rotor RPM
    nacelle_direction: Series[float] = pa.Field(nullable=True) # Nacelle direction

    controller_hubtemperature: Series[float] = pa.Field(nullable=True)
    gear_bearinghsgeneratorendtemperature: Series[float] = pa.Field(nullable=True)
    gear_bearinghsrotorendtemperature: Series[float] = pa.Field(nullable=True)
    generator_bearing2temperature: Series[float] = pa.Field(nullable=True)
    generator_coolingwatertemperature: Series[float] = pa.Field(nullable=True)
    hvtrafo_phase3temperature: Series[float] = pa.Field(nullable=True)
    hvtrafo_phase2temperature: Series[float] = pa.Field(nullable=True)
    nacelle_temperature: Series[float] = pa.Field(nullable=True)

    ## Extra
    hydraulic_oiltemperature: Series[float] = pa.Field(nullable=True)
    hydraulic_oilpressure: Series[float] = pa.Field(nullable=True)
    events_activealarms: Series[float] = pa.Field(nullable=True)
    grid_frequency: Series[float] = pa.Field(nullable=True)
    grid_settings_reactivepowerfactorvalue: Series[float] = pa.Field(nullable=True)
    grid_settings_reactivepowerreferencevalue: Series[float] = pa.Field(nullable=True)
    system_servicestateint: Series[float] = pa.Field(nullable=True)
    yaw_yawstatesyawcw_b: Series[bool] = pa.Field(nullable=True)