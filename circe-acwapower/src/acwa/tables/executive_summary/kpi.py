"""
acwa.tables.executive_summary.kpi

Validation schema for executive_summary_kpi table
"""

import pandera as pa
from pandera.typing import Series

LST_MONTHS = ["January", "February", "March", "April", "May", "June", "July", 
              "August", "September", "October", "November", "December", "All"]

class ExecutiveSummaryKPI(pa.DataFrameModel):
    """Schema for table executive_summary_kpi"""

    # Ids
    id_wf_period: Series[str] = pa.Field()
    id_wf: Series[str] = pa.Field()
    year: Series[str] = pa.Field() # We could coerce to int...
    month: Series[str] = pa.Field(isin=LST_MONTHS)

    energy: Series[float] = pa.Field()
    cp: Series[float] = pa.Field()
    contractual_available_time: Series[int] = pa.Field(ge=0)
    contractual_total_time: Series[int] = pa.Field(ge=0)
    count_data_ok: Series[int] = pa.Field(ge=0)
    count_data_total: Series[int] = pa.Field(ge=0)
    manufacturer_performance_loss: Series[float] = pa.Field()
    wind_speed: Series[float] = pa.Field(ge=0)
    p50: Series[float] = pa.Field(ge=0)
    p75: Series[float] = pa.Field(ge=0)
    p90: Series[float] = pa.Field(ge=0)
    p99: Series[float] = pa.Field(ge=0)
    contractual_availability: Series[float] = pa.Field(ge=0, le=100)
    PR_manufact: Series[float] = pa.Field(ge=0)
    overtemperature_percentage: Series[float] = pa.Field(ge=0, le=100)
