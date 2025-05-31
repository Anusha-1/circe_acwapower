"""
acwa.tables.maintenance

Validation schema for maintenance table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class MaintenanceSchema(pa.DataFrameModel):
    """Schema for table maintenance"""

    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 
    start_datetime: Series[datetime] = pa.Field() # Timestamp
    end_datetime: Series[datetime] = pa.Field() # Timestamp

    duration: Series[int] = pa.Field()
    duration_hours: Series[float] = pa.Field()
    cumulative_duration_hours: Series[float] = pa.Field()
