"""
acwa.tables.wf_config

Validation schema for wf_config table
"""

import pandera as pa
from pandera.typing import Series

class interpolPCConfigSchema(pa.DataFrameModel):
    """Schema for table power_curves"""

    pc_id: Series[str] = pa.Field() # Id for pc associated to range and density; unique
    id_wtg_complete: Series[str] = pa.Field() #id associated to wtg
    concept: Series[str] = pa.Field()
    period: Series[str] = pa.Field() #origin of the data in the table, if calculated will be hisotical, 6 months, 60 days,...
    sector_name: Series[str] = pa.Field() # Sector
    density: Series[str] = pa.Field()
    wind_speed: Series[float] = pa.Field(ge=0,lt=40) # windspeed been associated to pc
    power: Series[float] = pa.Field(nullable=True) # power from power curve in kw
    sigma: Series[float] = pa.Field(ge=0, nullable=True) # std. dev of the power curve
    wf_name: Series[str] = pa.Field()
    wtg_name: Series[str] = pa.Field()
    id_group_complete: Series[str] = pa.Field()
    group: Series[str] = pa.Field()
    
