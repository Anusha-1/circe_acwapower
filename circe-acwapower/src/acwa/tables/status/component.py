"""
acwa.tables.status.component

Validation schema for Status Component table
"""

import pandera as pa
from pandera.typing import Series

class StatusComponentSchema(pa.DataFrameModel):
    """Schema for table status_component table"""

    id_wtg_complete: Series[str] = pa.Field()  # Complete turbine id
    component: Series[str] = pa.Field()
    code: Series[int] = pa.Field()
    description: Series[str] = pa.Field()
    temperature: Series[float] = pa.Field(nullable=True)
    overtemperature: Series[int] = pa.Field() # 0 False and 1 True