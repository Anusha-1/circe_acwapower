"""
acwa.tables.aggregation.tower_acceleration

Validation schema for tower_acceleration_1day
"""

from datetime import date

import pandera as pa
from pandera.typing import Series

class TowerAcceleration1DaySchema(pa.DataFrameModel):
    """Schema for table tower_acceleration_1day"""

    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 
    day: Series[date] = pa.Field() # Day
    acceleration_binned: Series[float] = pa.Field()
    direction: Series[str] = pa.Field(isin=['X','Y'])
    count: Series[int] = pa.Field()