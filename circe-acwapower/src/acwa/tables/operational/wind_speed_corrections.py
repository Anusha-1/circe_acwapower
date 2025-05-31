"""
acwa.tables.wind_speed_corrections

Validation schema for wind_speed_corrections table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class WindSpeedCorrectionsSchema(pa.DataFrameModel):
    """Schema for table wind_speed_corrections"""

    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 
    timestamp: Series[datetime] = pa.Field() # Timestamp
    wind_speed_corrected: Series[float] = pa.Field(nullable=True) # Wind Speed corrected
    density_corrected: Series[str] = pa.Field() # Density reference applied
