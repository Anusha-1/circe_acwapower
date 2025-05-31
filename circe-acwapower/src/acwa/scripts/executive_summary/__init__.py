"""
acwa.scripts.executive_summary

Module with scripts for executive summary
"""

from .alarms import main as obtain_executive_summary_alarms
from .kpis import main as obtain_executive_summary_kpis

__all__ = [
    obtain_executive_summary_alarms, 
    obtain_executive_summary_kpis
]