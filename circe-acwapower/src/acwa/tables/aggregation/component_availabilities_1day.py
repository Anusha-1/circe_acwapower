"""
acwa.tables.component_availabilities_1day

Validation schema for component_availabilities_1day table
"""

from datetime import date

import pandera as pa
from pandera.typing import Series

class ComponentAvailabilities1DaySchema(pa.DataFrameModel):
    """Schema for table component_availabilities_1day"""

    id_wf: Series[str] = pa.Field() # Wind Farm id
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id  

    day: Series[date] = pa.Field() # Day
    
    component: Series[str] = pa.Field() # Manufacturer concept
    
    duration: Series[float] = pa.Field() # Duration of the alarm (in seconds)
    losses: Series[float] = pa.Field() # Losses associated with the alarm (kWh)
    
    # Add more ... (More classification types?)
