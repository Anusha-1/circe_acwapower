"""
acwa.tables.power_curves.pc_metadata

Validation schema for pc_metadata table
"""

import pandera as pa
from pandera.typing import Series

class PCMetadataSchema(pa.DataFrameModel):
    """Schema for table pc_metadata table"""

    pc_id: Series[str] = pa.Field(unique=True) # id from power curve: concatenating characteristcs
    id_wtg_complete: Series[str] = pa.Field() # id wtg complete
    concept: Series[str] = pa.Field()
    period: Series[str] = pa.Field() # 
    sector_name: Series[str] = pa.Field() # code of reference power curve
    density: Series[str] = pa.Field() # density of the power curve
    main: Series[bool] = pa.Field() # True if it is the main sector
