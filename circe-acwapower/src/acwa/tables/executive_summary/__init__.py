"""
acwa.tables.executive_summary

Collection of tables schemas for executive summary
"""

from .alarms import ExecutiveSummaryAlarms
from .kpi import ExecutiveSummaryKPI

__all__ = [ExecutiveSummaryKPI, ExecutiveSummaryAlarms]
