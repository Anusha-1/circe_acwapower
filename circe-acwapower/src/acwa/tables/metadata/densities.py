"""
acwa.tables.metadata.densities

Validation schema for densities table
"""

import pandera as pa
from pandera.typing import Series

class DensitiesSchema(pa.DataFrameModel):
    """Schema for table densities"""
    
    id_wf: Series[str] = pa.Field() # Wind Farm
    density: Series[float] = pa.Field(gt=0)
    main: Series[int] = pa.Field()
