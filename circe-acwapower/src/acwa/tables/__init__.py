"""
acwa.tables

Module to keep validation schemas for the tables
"""

from .metadata import (
    AEPSchema,
    AlarmsMetadataSchema,
    DensitiesSchema,
    SectorsSchema,
    TemperatureSignalsSchema,
    WfConfigSchema,
    WtgConfigSchema,
    MetMastMetadataSchema,
    ReliabilityModelsSchema
)

from .power_curves import (
    PowerCurvesSchema,
    PCMetadataSchema,
    interpolPCConfigSchema
)

from .alarms import (
    AlarmsLossesSchema,
    BasicAlarmsSchema,
    InputAlarmsSchema,
    TreatedEventsSchema
)

from .operational import(
    Input10minSchema,
    Input1minSchema,
    Basic10minSchema,
    Oper1minSchema,
    Oper10minSchema,
    MaintenanceSchema,
    MetMastSchema,
    WindSpeedCorrectionsSchema
)

from .aggregation import (
    ComponentAvailabilities1DaySchema,
    DynamicYawSchema,
    LapmAnalysisSchema,
    ManufacturerAvailabilities1DaySchema,
    MaxPowerMisallignmentSchema,
    Oper1DaySchema,
    PerformanceRatioSchema,
    TowerAcceleration1DaySchema,
    TreatedEvents1DaySchema
)

from .status import (
    StatusSchema,
    StatusComponentSchema,
    StatusMetMastSchema
)

from .executive_summary import (
    ExecutiveSummaryKPI,
    ExecutiveSummaryAlarms
)

from .general_metadata import MetadataSchema

__all__ = [

    MetadataSchema,

    ## Metadata Tables
    AEPSchema,
    AlarmsMetadataSchema,
    DensitiesSchema,
    SectorsSchema,
    TemperatureSignalsSchema,
    WfConfigSchema,
    WtgConfigSchema,
    ReliabilityModelsSchema,
    MetMastMetadataSchema,

    ## Power Curves Tables
    PowerCurvesSchema,
    PCMetadataSchema,
    interpolPCConfigSchema,   

    ## Alarms Tables
    InputAlarmsSchema,
    BasicAlarmsSchema,
    AlarmsLossesSchema,
    TreatedEventsSchema,

    ## Operational
    Input10minSchema,
    Input1minSchema,
    Basic10minSchema,
    Oper10minSchema,
    Oper1minSchema,
    MaintenanceSchema,
    MetMastSchema,
    WindSpeedCorrectionsSchema,

    ## Aggregation Tables
    ComponentAvailabilities1DaySchema,
    DynamicYawSchema,
    LapmAnalysisSchema,
    ManufacturerAvailabilities1DaySchema,
    MaxPowerMisallignmentSchema,
    Oper1DaySchema,
    PerformanceRatioSchema,
    TowerAcceleration1DaySchema,
    TreatedEvents1DaySchema,

    ## Status Tables
    StatusSchema,
    StatusMetMastSchema,
    StatusComponentSchema,

    ## Executive Summary Tables
    ExecutiveSummaryKPI,
    ExecutiveSummaryAlarms,
    
    
]
