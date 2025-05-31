"""
acwa.tables.metadata

Validation schema for metadata table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class MetadataSchema(pa.DataFrameModel):
    """Schema for table metadata"""

    schema: Series[str] = pa.Field() # Name of the schema
    table: Series[str] = pa.Field() # Name of the table
    last_update: Series[datetime] = pa.Field() # Datetime of last update
