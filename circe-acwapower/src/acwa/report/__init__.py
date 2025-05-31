"""
acwa.report

Classes for reports
"""

from .daily import DailyReportPDF
from .test_table_data import generate_test_table1_data
from .test_table_data2 import generate_test_table2_data
from .test_table_data3 import generate_test_table3_data
from .test_table_data4 import generate_test_table4_data
from .test_table_data9 import generate_test_table9_data
from .table_wind_speed import create_wind_speed_table
from .table_tarif import create_prod_oper
from .table_net_generation import create_total_net_generation
from .table_availability import create_table_availability
from .table_alarms import create_table_alarms
from .table_report_plot import create_table_for_report_plot
from .test_table_plot import generate_test_table_plot

__all__ = [
    DailyReportPDF, 
    generate_test_table1_data, 
    generate_test_table2_data, 
    generate_test_table3_data, 
    generate_test_table4_data,
    generate_test_table9_data,
    create_wind_speed_table,
    create_prod_oper,
    create_total_net_generation,
    create_table_availability,
    create_table_alarms,
    create_table_for_report_plot,
    generate_test_table_plot
    ]
