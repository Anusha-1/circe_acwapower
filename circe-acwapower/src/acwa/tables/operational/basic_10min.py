"""
acwa.tables.basic_10min_with_alarms

Validation schema for oper_10min table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series
from pandera.dtypes import Int32

class Basic10minSchema(pa.DataFrameModel):
    """Schema for table basic_10min"""

    id_wf: Series[str] = pa.Field() # Wind Farm
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 

    timestamp: Series[datetime] = pa.Field() # Timestamp
    wind_speed: Series[float] = pa.Field(nullable=True) # Wind Speed
    power: Series[float] = pa.Field(nullable=True) # Power
    temperature: Series[float] = pa.Field(nullable=True) # Temperature
    wind_direction: Series[float] = pa.Field(nullable=True) # Wind direction
    nacelle_direction: Series[float] = pa.Field(nullable=True) # Nacelle direction
    rotor_rpm: Series[float] =pa.Field(nullable=True) # Rotor RPM
    generator_rpm: Series[float] =pa.Field(nullable=True) # Generator RPM
    lambda_parameter:Series[float] = pa.Field(nullable=True) #tip speed ratio 

    density: Series[float] = pa.Field(gt=0, nullable= True)
    wind_speed_corrected: Series[float] = pa.Field(nullable=True)
    sector_name: Series[str] = pa.Field(nullable=True)

    code: Series[int] = pa.Field() # Main alarm

    lambda_parameter_binned:Series[float] = pa.Field(nullable=True)
    wind_speed_corrected_binned:Series[float] = pa.Field(nullable=True)
    cp: Series[float] = pa.Field(nullable=True,ge=0) # Cp Power/0.5*ro*A*V**3

    ## Yaw
    angle_deviation: Series[float] = pa.Field(nullable=True, le=180, gt=-180)
    angle_deviation_sector: Series[str] = pa.Field(nullable=True)
    angle_deviation_sign: Series[Int32] = pa.Field(nullable=True, isin=[-1,1])

    pitch_angle_average: Series[float] = pa.Field(nullable=True)

    ## Temperatures
    controller_hubtemperature: Series[float] = pa.Field(nullable=True)
    gear_bearinghsgeneratorendtemperature: Series[float] = pa.Field(nullable=True)
    gear_bearinghsrotorendtemperature: Series[float] = pa.Field(nullable=True)
    generator_bearing2temperature: Series[float] = pa.Field(nullable=True)
    generator_coolingwatertemperature: Series[float] = pa.Field(nullable=True)
    hvtrafo_phase3temperature: Series[float] = pa.Field(nullable=True)
    hvtrafo_phase2temperature: Series[float] = pa.Field(nullable=True)
    nacelle_temperature: Series[float] = pa.Field(nullable=True)

