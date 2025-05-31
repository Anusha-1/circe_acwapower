"""
acwa.tables.metadata

Collection of schemas for metadata tables
"""

from .AEP_config import AEPSchema
from .alarms import AlarmsMetadataSchema
from .densities import DensitiesSchema
from .reliability_models import ReliabilityModelsSchema
from .sectors import SectorsSchema
from .temperature_signals import TemperatureSignalsSchema
from .wf_config import WfConfigSchema
from .wtg_config import WtgConfigSchema
from .met_mast import MetMastMetadataSchema

__all__ = [
    AEPSchema,
    AlarmsMetadataSchema,
    DensitiesSchema,
    ReliabilityModelsSchema,
    SectorsSchema,
    TemperatureSignalsSchema,
    WfConfigSchema,
    WtgConfigSchema,
    MetMastMetadataSchema
]