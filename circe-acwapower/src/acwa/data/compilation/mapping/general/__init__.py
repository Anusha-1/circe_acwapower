"""
acwa.data.compilation.mapping.general

General functions to map tables
"""

from .turbine_id import map_from_table_with_turbine_id
from .turbine_columns import map_from_table_with_turbine_columns

__all__ = [
    map_from_table_with_turbine_id,
    map_from_table_with_turbine_columns
]
