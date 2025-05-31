"""
acwa.tables.metadata.alarms

Validation schema for alarms_metadata table
"""

import pandera as pa
from pandera.typing import Series

class AlarmsMetadataSchema(pa.DataFrameModel):
    """Schema for table alarms_metadata"""
    
    alarm_name: Series[str] = pa.Field() #concatenation of code and description. asked by Powerbi team
    code: Series[int] = pa.Field(unique=True) # Code of the alarm

    description: Series[str] = pa.Field() # Description of the alarm
    legacy_type: Series[str] = pa.Field(isin=['Fault', 'Information', 'Warning', 'Custom'])
    manufacturer_availability: Series[str] = pa.Field()
    operational_availability: Series[str] = pa.Field(isin=['Available', 'NotAvailable'])
    severity_scale: Series[int] = pa.Field(ge=1, le=6)
    priority: Series[int] = pa.Field(ge=1, le=12)

    component: Series[str] = pa.Field()
    classification: Series[str] = pa.Field()
    status: Series[str] = pa.Field(
        isin=[
            "Running",
            "Stop",
            "Warning",
            "Underperforming",
            "Overtemperature",
            "Missing data",
        ]
    )
