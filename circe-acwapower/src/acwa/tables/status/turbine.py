"""
acwa.tables.status.turbine

Validation schema for status table
"""

from datetime import datetime

import pandera as pa
from pandera.typing import Series


class StatusSchema(pa.DataFrameModel):
    """Schema for table status table"""

    id_wf: Series[str] = pa.Field()  # Wind Farm
    id_wtg: Series[str] = pa.Field()  # Turbine id
    id_wtg_complete: Series[str] = pa.Field(unique=True)  # Complete turbine id
    timestamp: Series[datetime] = pa.Field()

    wind_speed: Series[float] = pa.Field(
        nullable=True
    )  # Maybe at the end it shouldn't be NaN
    power: Series[float] = pa.Field(nullable=True)
    temperature: Series[float] = pa.Field(nullable=True)
    wind_direction: Series[float] = pa.Field(le=360, nullable=True)  # Wind direction

    status: Series[str] = pa.Field(
        isin=[
            "Running",
            "Stop",
            "Warning",
            "Underperforming",
            "Overtemperature",
            "Communication loss",
        ]
    )
    code: Series[int] = pa.Field()  # Code
    description: Series[str] = pa.Field()  # Description of the alarm

    energy_24h: Series[float] = pa.Field(nullable=True)
    energy_mtd: Series[float] = pa.Field(nullable=True)
    energy_ytd: Series[float] = pa.Field(nullable=True)

    mtbf: Series[float] = pa.Field(nullable=True)
    mttr: Series[float] = pa.Field(nullable=True)

    pr_mtd: Series[float] = pa.Field(nullable=True)
    pr_ytd: Series[float] = pa.Field(nullable=True)

    data_availability: Series[float] = pa.Field(ge=0, le=100) # count_data_ok / count_data_total
    wind_availability: Series[float] = pa.Field(ge=0, le=100) # wind_available_time / wind_total_time * 100
    operation_I_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    operation_II_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    operation_III_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    technical_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    contractual_availability: Series[float] = pa.Field(ge=0, le=100, nullable=True) # Available / Total
    production_user_I_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential
    production_user_II_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential
    production_manufacturer_availability: Series[float] = pa.Field(nullable=True) # Availability = Actual / Potential

    reliable: Series[bool] = pa.Field(nullable=False) # True if turbine is Ok, False if it has overtemperature