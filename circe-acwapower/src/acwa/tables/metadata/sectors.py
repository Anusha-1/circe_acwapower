"""
acwa.tables.sectors

Validation schema for sectors table
"""

import pandera as pa
from pandera.typing import Series

class SectorsSchema(pa.DataFrameModel):
    """Schema for table sectors table"""

    id_wtg_complete: Series[str] = pa.Field() # id wtg complete
    sector_name: Series[str] = pa.Field() # code of reference power curve
    sector_ini: Series[int] = pa.Field(ge=0,le=360) # direction range limit
    sector_fin: Series[int] = pa.Field(ge=0,le=360) # direction range limit
    main: Series[bool] = pa.Field() # True if is the main sector of the turbine
