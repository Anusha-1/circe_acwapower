from fpdf import FPDF, XPos, YPos
import webbrowser
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import subprocess
import platform
import os
import shutil
import logging
import pathlib
import pandas as pd
import acwa.mensual_report as m_rep
from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.db import read_table_as_df

DICT_WF = {"Kh": "Khalladi", "Az": "Azerbaijan"}


def main(
    id_wf: str,
    mode_debug: bool = False,
    date_report: datetime | None = None,
    year_offset: bool = False,
    annual_mode: bool = False
):
    config = read_config()
    format_basic_logging(config["log"])
    if annual_mode:
        logging.info("--------------- START SCRIPT: report.yearly -----------------")
        output_path = pathlib.Path("data", "output", "reports", f"yearly_{date.today()}.pdf")
    else:
        logging.info("--------------- START SCRIPT: report.monthly -----------------")
        output_path = pathlib.Path("data", "output", "reports", f"monthly_{date.today()}.pdf")
        
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if date_report is None:
        date_report = date.today()
        date_report = datetime(date_report.year, date_report.month, date_report.day)
        if year_offset:
            date_report = date_report - relativedelta(year=2023) #- relativedelta(months=1)
    date_report = pd.to_datetime(date_report)
    logging.info(f"Report date: {date_report}")


    # Initialize PDF
    monthly_report_pdf = m_rep.MonthlyReportPDF(title = f'Khalladi Wind Farm Summary Report', author= 'ACWA Power', date= date_report, annual_mode=annual_mode)

    tmp_folder = pathlib.Path("data", "output", "figures")
    tmp_folder.mkdir(parents=True, exist_ok=True)

    logging.info('load necessary data')
    data_lst = m_rep.load_data(date_report, id_wf,['oper_10min', 'aep_table', 'wtg_config', 'oper_1day'], annual_mode=annual_mode)
    
    logging.info('Creating wf kpi pages.')
    monthly_report_pdf.add_page(orientation='P')
    monthly_report_pdf.add_section_header('Section 1 : KPI Overview')
    monthly_report_pdf.add_paragraph("The current section will show the main KPI's to control the wind farm")
    monthly_report_pdf.add_wf_kpi_page(date_report, id_wf, data_lst)

    logging.info('creating bar plot for wf')
    monthly_report_pdf.add_page(orientation='P')
    monthly_report_pdf.add_wf_bar_plot_power(date_report, id_wf, data_lst, tmp_folder)

    logging.info('creating bar plot for wf')
    monthly_report_pdf.add_wf_bar_plot_ws(date_report, id_wf, data_lst, tmp_folder)


    logging.info('load data for wtgs')
    weibull_data = read_table_as_df('weibull_distribution', config['db'], 'vis')
    pc_data = read_table_as_df('power_curves', config['db'], 'vis')
    pc_metadata = read_table_as_df('pc_metadata',config['db'], 'vis')
    densities = read_table_as_df('densities', config['db'], 'vis')
    wtg_config = read_table_as_df('wtg_config', config['db'], 'vis')
    wtg_lst = wtg_config[wtg_config['id_wf']== id_wf]['id_wtg']

    # wtg_lst = [wtg_lst[28]] #[wtg_lst[0],wtg_lst[1],wtg_lst[3]] ## to be able to debug just one turbine
    wf_name = DICT_WF[id_wf]
    
    oper_10min = read_table_as_df('oper_10min', config['db'], 'vis')
    oper_10min = oper_10min[['id_wtg_complete','timestamp','wind_speed','power','wind_speed_corrected','sector_name', 'wind_direction']]
    


    logging.info('loop for every turbine in wind farm')
    monthly_report_pdf.add_page(orientation='P')
    monthly_report_pdf.add_section_header('Section 2 : WTG')
    monthly_report_pdf.add_paragraph('Current section will cover operational analysis per wind turbine')
    
    for i, wtg in enumerate(wtg_lst):
        logging.info(wtg)
        wtg_name = id_wf + '-' + wtg
        i = i+1
          
        monthly_report_pdf.add_weibull_dist(
            wtg_name= wtg_name,
            date=date_report, 
            oper_10min=oper_10min, 
            tmp_folder=tmp_folder,
            i=i,
            wtg=wtg,
            annual_mode= annual_mode)

        monthly_report_pdf.add_power_curve(
            wtg_name= wtg_name,
            id_wf=  id_wf,
            date = date_report, 
            pc_data= pc_data, 
            pc_metadata=pc_metadata,
            oper_10min=oper_10min, 
            densities= densities, 
            tmp_folder=tmp_folder, 
            i= i, 
            wtg=wtg,
            annual_mode = annual_mode)
        
        monthly_report_pdf.add_wind_rose(
            date =date_report,
            wtg_name=wtg_name, 
            oper_10min= oper_10min,
            tmp_folder=tmp_folder, 
            i=i, 
            wtg=wtg,
            annual_mode=annual_mode)

    # Save and open the PDF
    if annual_mode:
        output_path = pathlib.Path("data", "output", "reports", f"annual_{datetime.strftime(date_report, '%Y-%B')}.pdf")

    else:
        output_path = pathlib.Path("data", "output", "reports", f"monthly_{datetime.strftime(date_report, '%Y-%B')}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    monthly_report_pdf.output(output_path)
    webbrowser.open(output_path)


    if os.path.exists(tmp_folder):
        # Remove the folder and all its contents
        try:
            shutil.rmtree(tmp_folder)
            print(f"Folder '{tmp_folder}' and its contents have been removed.")
        except PermissionError as e:
            print(f"PermissionError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Folder '{tmp_folder}' does not exist.")
    

    print(f"PDF file created and opened successfully.")





if __name__ == "__main__":

    main(
        "Kh", # ID of the Wind Farm 
        # mode_debug=True, 
        date_report=datetime(2023, 9,30), 
        year_offset=True,
        annual_mode=True)
