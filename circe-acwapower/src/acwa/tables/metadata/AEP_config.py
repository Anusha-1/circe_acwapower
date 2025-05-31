
import pandera as pa
import datetime
from pandera.typing import Series

class AEPSchema(pa.DataFrameModel):
    """Schema for table AEP_table table"""
    id_wf: Series[str] = pa.Field() # Wind Farm
    id_wtg: Series[str] = pa.Field() # Turbine id
    id_wtg_complete: Series[str] = pa.Field() # Complete turbine id 

    timestamp: Series[datetime.datetime] = pa.Field()  #current month
    

    month_weight:Series[float] = pa.Field(ge=0, le=1) #month weight on the overall AEP
    wtg_weight:Series[float] = pa.Field(ge=0, le=1) #wtg weight over wind farm 
    factor:Series[float] = pa.Field(ge=0, le=1) # wtg weight over wind farm on current month


    #AEP by probabilities assuming normal distribution
    P50:Series[float] = pa.Field() 
    P75:Series[float] = pa.Field()
    P90:Series[float] = pa.Field()
    P99:Series[float] = pa.Field()

    energy_production:Series[float] = pa.Field(nullable=True) #month energy production by turbine        