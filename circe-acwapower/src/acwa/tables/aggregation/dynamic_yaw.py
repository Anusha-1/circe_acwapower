"""
acwa.tables.dynamic_yaw

Validation schema for dynamic_yaw table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class DynamicYawSchema(pa.DataFrameModel):
    """Schema for table dynamic_yaw"""

    id_wtg_complete: Series[str] = pa.Field()
    hour: Series[datetime] = pa.Field()
    changes: Series[float] = pa.Field(ge=0, le=60)
    label: Series[str] = pa.Field()
    