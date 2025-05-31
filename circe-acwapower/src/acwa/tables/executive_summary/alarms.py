"""
acwa.tables.executive_summary.alarms

Validation schema for executive_summary_alarms table
"""

import pandera as pa
from pandera.typing import Series

LST_MONTHS = ["January", "February", "March", "April", "May", "June", "July", 
              "August", "September", "October", "November", "December", "All"]


class ExecutiveSummaryAlarms(pa.DataFrameModel):
    """Schema for table executive_summary_alarms"""

    # Ids
    id_wf_period: Series[str] = pa.Field()
    id_wf: Series[str] = pa.Field()
    year: Series[str] = pa.Field() # We could coerce to int...
    month: Series[str] = pa.Field(isin=LST_MONTHS)

    id_wtg_complete: Series[str] = pa.Field()

    code: Series[int] = pa.Field()

    total_duration: Series[float] = pa.Field(ge=0) # Seconds
    total_losses: Series[float] = pa.Field(ge=0) # kWh
