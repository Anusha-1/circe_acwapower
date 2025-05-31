"""
acwa.tables.lapm_analysis

Validation schema for lapm_analysis table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class LapmAnalysisSchema(pa.DataFrameModel):
    """Schema for table lapm_analysis"""

    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 
    timestamp: Series[datetime] = pa.Field() # Timestamp
    wind_speed: Series[float] = pa.Field(nullable=True) # Wind Speed
    power: Series[float] = pa.Field(nullable=True) # Power
    wind_direction: Series[float] = pa.Field(nullable=True) # Wind direction
    sector_name: Series[str] = pa.Field(nullable=True)
    identified_sector: Series[str] = pa.Field(nullable=True)
