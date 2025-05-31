"""
acwa.tables.oper_1day

Validation schema for oper_1day table
"""

from datetime import date

import pandera as pa
from pandera.typing import Series

class Oper1DaySchema(pa.DataFrameModel):
    """Schema for table oper_1day"""

    id_wf: Series[str] = pa.Field() # Wind Farm
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 

    day: Series[date] = pa.Field() # Day

    wind_speed: Series[float] = pa.Field(nullable=True)
    wind_speed_corrected: Series[float] = pa.Field(nullable=True)

    count_data_ok: Series[int] = pa.Field(ge=0, le=144) # Number of correct 10-min
    count_data_total: Series[int] = pa.Field(ge=0, le=144) # It should be 144, unless the first or last day is not complete
    data_availability: Series[float] = pa.Field(ge=0, le=100) # count_data_ok / count_data_total

    energy: Series[float] = pa.Field() # Energy produced (MWh)
    producible: Series[float] = pa.Field() # Producible energy (MWh)
    loss: Series[float] = pa.Field() # Energy lost (MWh)
    
    # Availabilities (ask for definitions)
    # All times in minutes
    wind_available_time: Series[int] = pa.Field() # Time with wind speed between start (~3m/s) and stop (~20 m/s)
    wind_total_time: Series[int] = pa.Field() # 24 h. per day ?
    wind_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # wind_available_time / wind_total_time * 100
    operation_I_available_time: Series[int] = pa.Field() # Available time
    operation_I_total_time: Series[int] = pa.Field() # Avilable + Unavailable Time
    operation_I_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    operation_II_available_time: Series[int] = pa.Field() # Available time
    operation_II_total_time: Series[int] = pa.Field() # Avilable + Unavailable Time
    operation_II_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    operation_III_available_time: Series[int] = pa.Field() # Available time
    operation_III_total_time: Series[int] = pa.Field() # Avilable + Unavailable Time
    operation_III_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    technical_available_time: Series[int] = pa.Field() # Available time
    technical_total_time: Series[int] = pa.Field() # Avilable + Unavailable Time
    technical_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    contractual_available_time: Series[int] = pa.Field() # Available time
    contractual_total_time: Series[int] = pa.Field() # Avilable + Unavailable Time
    contractual_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total

    # Production-based availabilities
    actual_energy_user_I: Series[float] = pa.Field() # Actual energy
    potential_energy_user_I: Series[float] = pa.Field() # Potential energy
    production_user_I_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential
    actual_energy_user_II: Series[float] = pa.Field() # Actual energy
    potential_energy_user_II: Series[float] = pa.Field() # Potential energy
    production_user_II_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential
    actual_energy_manufacturer: Series[float] = pa.Field() # Actual energy
    potential_energy_manufacturer: Series[float] = pa.Field() # Potential energy
    production_manufacturer_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential

    # Other magnitudes
    cp: Series[float] = pa.Field(nullable=True) # Cp average
    production_ratio: Series[float] = pa.Field(nullable=True) # Power/Producible
    energy_availability: Series[float] = pa.Field(nullable=True) # Power/(power+loss) production_user_I_availability?

    manufacturer_performance_loss: Series[float] = pa.Field()
    historical_performance_loss: Series[float] = pa.Field()

    p50:Series[float] = pa.Field() 
    p75:Series[float] = pa.Field() 
    p90:Series[float] = pa.Field() 
    p99:Series[float] = pa.Field() 

    # Add more ...
    