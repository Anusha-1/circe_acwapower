"""
acwa.alarms.metadata

Registers for custom alarms in metadata table
"""

from .communication_loss import MISSING_DATA_METADATA
from .nonregistered import NONREGISTERED_METADATA
from .underperforming import UNDERPERFORMING_METADATA

__all__ = [
    NONREGISTERED_METADATA, 
    UNDERPERFORMING_METADATA, 
    MISSING_DATA_METADATA]
