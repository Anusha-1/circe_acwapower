"""
acwa.tables.temperature_signals

Validation schema for temperature_signals table
"""

import pandera as pa
from pandera.typing import Series

class TemperatureSignalsSchema(pa.DataFrameModel):
    """Schema for table temperature_signals table"""
    
    name_in_origin: Series[str] = pa.Field()
    main_component: Series[str] = pa.Field()
    subcomponent: Series[str] = pa.Field()
    name: Series[str] = pa.Field()

    # Add more ? ...
