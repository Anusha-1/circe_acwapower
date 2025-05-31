"""
acwa.tables.metadata.reliability_models

Metadata table with fitted models
"""

from datetime import datetime
import pandera as pa
from pandera.typing import Series

class ReliabilityModelsSchema(pa.DataFrameModel):
    """Schema for table reliability_models table"""

    signal: Series[str] = pa.Field() # signal
    group: Series[str] = pa.Field() # group
    oper_stat: Series[str] = pa.Field() # oper stat: min, max, median, ...
    quantile: Series[float] = pa.Field()
    last_update: Series[datetime] = pa.Field()
