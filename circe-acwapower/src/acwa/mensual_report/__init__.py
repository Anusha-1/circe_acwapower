"""
acwa.report

Classes for reports
"""

from .monthly import MonthlyReportPDF
from .monthly_data import get_monthly_kpi, get_monthly_power_wf_graph, load_data, get_monthly_ws_wf_graph, get_monthly_wtg_kpi


__all__ = [
    MonthlyReportPDF, 
    load_data,
    get_monthly_kpi,
    get_monthly_power_wf_graph,
    get_monthly_ws_wf_graph,
    get_monthly_wtg_kpi,
    
    
    ]
