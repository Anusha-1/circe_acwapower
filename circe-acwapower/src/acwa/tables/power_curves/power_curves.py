"""
acwa.tables.power_curves.power_curves

Validation schema for power_curves table
"""

import pandera as pa
from pandera.typing import Series

class PowerCurvesSchema(pa.DataFrameModel):
    """Schema for table power_curves"""

    pc_id: Series[str] = pa.Field() # Id for pc associated to range and density; unique
    bin: Series[float] = pa.Field(ge=0,lt=40) # windspeed been associated to pc
    power: Series[float] = pa.Field(nullable=True) # power from power curve in kw
    sigma: Series[float] = pa.Field(ge=0, nullable=True) # std. dev of the power curve
