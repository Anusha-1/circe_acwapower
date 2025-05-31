"""
acwa.tables.basic_input_alarms

Validation schema for input_alarms table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class InputAlarmsSchema(pa.DataFrameModel):
    """Schema for table input_alarms"""

    id_wf: Series[str] = pa.Field() # Wind Farm id
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id  

    code: Series[int] = pa.Field() # Code
    description: Series[str] = pa.Field() # Description of the alarm
    start_datetime: Series[datetime] = pa.Field() # Start of the event
    end_datetime: Series[datetime] = pa.Field(nullable=True) # End of the event
    
    # Extra data at raw events
    serial_number: Series[int] = pa.Field()
    event_type: Series[str] = pa.Field()
    severity: Series[int] = pa.Field()
    remark: Series[str] = pa.Field()
