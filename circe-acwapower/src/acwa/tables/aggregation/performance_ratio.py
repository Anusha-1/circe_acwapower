"""
acwa.tables.power_curves

Validation schema for power_curves table
"""

import pandera as pa
from pandera.typing import Series

class PerformanceRatioSchema(pa.DataFrameModel):
    """Schema for table power_curves"""

    id_wtg_complete: Series[str] = pa.Field() # Turbine id
   
    concept: Series[str] = pa.Field()
    period: Series[str] = pa.Field() # period of the used data in calc of Performance Ratio
    PR_hist: Series[float] = pa.Field() # PR calculated with historical power curve, corresponds also the same period of data
    PR_manufact: Series[float] = pa.Field() # PR calculated with manufacturer power curve, correspondsonly to main Power Curve
