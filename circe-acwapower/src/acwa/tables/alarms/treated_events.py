"""
acwa.tables.treated_events

Validation schema for treated_events table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series

class TreatedEventsSchema(pa.DataFrameModel):
    """Schema for table treated_events"""

    id_wf: Series[str] = pa.Field() # Wind Farm id
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 

    code: Series[int] = pa.Field() # Code
    description: Series[str] = pa.Field() # Description of the alarm
    component: Series[str] = pa.Field() # Affected component
    start_datetime: Series[datetime] = pa.Field() # Start of the event
    end_datetime: Series[datetime] = pa.Field() # End of the event
    duration: Series[int] = pa.Field() # Duration of the alarm (in seconds?)
    ongoing: Series[bool] = pa.Field() # If the alarm is currently active

    losses: Series[float] = pa.Field(nullable=True) # Losses associated with the alarm

    time_since_previous_alarm: Series[int] = pa.Field(nullable=True) # Time in seconds until next alarm
    time_since_previous_same_alarm: Series[int] = pa.Field(nullable=True) # Time in seconds until next alarm of the same code

    serial_number: Series[int] = pa.Field(nullable=True)
    event_type: Series[str] = pa.Field(nullable=True)
    severity: Series[int] = pa.Field(nullable=True)
    remark: Series[str] = pa.Field(nullable=True)

    severity_scale: Series[int] = pa.Field(ge=1, le=6)
    legacy_type: Series[str] = pa.Field()
    classification: Series[str] = pa.Field()
    manufacturer_availability: Series[str] = pa.Field(nullable=True)
    priority: Series[int] = pa.Field(ge=1, le=12)

    ## Clasificaciones de alarmas

    # Add more ...
