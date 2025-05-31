"""
acwa.tables.metadata.met_mast

Validation schema for met_mast_metadata table
"""

import pandera as pa
from pandera.typing import Series

class MetMastMetadataSchema(pa.DataFrameModel):
    """Schema for table met_mast_metadata table"""

    wf_name: Series[str] = pa.Field() # wf name
    met_mast_id: Series[str] = pa.Field() # id met mast

    latitude: Series[float] = pa.Field(ge=-90, le=90) # Latitude
    longitude: Series[float] = pa.Field(ge=-180, le=180) # Longitude
    elevation: Series[int] = pa.Field() #met mast elevation
    
    ws_height: Series[float] = pa.Field(ge=0) # windspeed sensor height
    dir_height: Series[float] = pa.Field(ge=0)# windvane sensor height
    pres_height: Series[float] = pa.Field(ge=0) # pressure sensor height
    temp_height: Series[float] = pa.Field(ge=0) # temperature sensor height
    rh_height: Series[float] = pa.Field(ge=0) # relative humidity sensor height
    rain_height: Series[float] = pa.Field(ge=0) # rain sensor height
