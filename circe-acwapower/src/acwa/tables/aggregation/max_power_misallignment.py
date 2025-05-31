"""
acwa.tables.max_power_misallignment

Validation schema for max_power_misallignment table
"""

import pandera as pa
from pandera.typing import Series

class MaxPowerMisallignmentSchema(pa.DataFrameModel):
    """Schema for table max_power_misallignment"""
    
    id_wtg_complete: Series[str] = pa.Field()
    wind_speed_bin: Series[float] = pa.Field()
    period: Series[str] = pa.Field()
    angle_deviation_bin: Series[float] = pa.Field()
    power_mean: Series[float] = pa.Field()

    # fitted_max: Series[float] = pa.Field(nullable=True)
