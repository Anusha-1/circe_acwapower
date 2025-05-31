"""
acwa.tables.status.met_mast

Validation schema for status_met_mast table
"""


import pandera as pa
from datetime import datetime
from pandera.typing import Series

class StatusMetMastSchema(pa.DataFrameModel):
    """Schema for table status_met_mast table"""
    id_wtg_config:Series[str]=pa.Field()
    met_mast_id: Series[str] =pa.Field()
    wf_name: Series[str] = pa.Field()
    timestamp: Series[datetime] = pa.Field(nullable=True)
    type:Series[str] = pa.Field()
    air_density: Series[float] = pa.Field(nullable=True,gt=0,lt=3) #(kg/m3)
    pressure: Series[float] = pa.Field(nullable=True,gt=600, lt=1200) #(hpa)
    battery: Series[float] = pa.Field(nullable=True,ge=0, lt=20) #(V)
    relative_humidity: Series[float] = pa.Field(nullable=True,ge=0,lt=120) #(%)
    rain: Series[float] = pa.Field(nullable=True,le=7000) #(mV)
    temperature: Series[float] = pa.Field(nullable=True,ge=-60, lt=100) # (ºC)
    wind_direction: Series[float] = pa.Field(nullable=True,ge=0,le=365) # (º)
    wind_speed: Series[float] = pa.Field(nullable=True,ge=0,le=60) # (m/s)
    