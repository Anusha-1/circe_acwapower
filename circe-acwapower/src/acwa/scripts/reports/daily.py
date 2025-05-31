"""
acwa.scripts.reports.daily

Creates a daily report
"""

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
import pathlib

import acwa.db as db
import acwa.report as rep

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.files import read_json

DICT_WF = {"Kh": "Khalladi", "Az": "Azerbaijan"}


def main(
    id_wf: str,
    mode_debug: bool = False,
    date_report: datetime | None = None,
    year_offset: bool = False,
):
    config = read_config()
    format_basic_logging(config["log"])

    logging.info("--------------- START SCRIPT: report.daily -----------------")
    output_path = pathlib.Path("data", "output", "reports", f"daily_{date.today()}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if date_report is None:
        date_report = date.today()
        date_report = datetime(date_report.year, date_report.month, date_report.day)
        if year_offset:
            date_report = date_report - relativedelta(year=2023)
    logging.info(f"Report date: {date_report}")

    daily_report_pdf = rep.DailyReportPDF()
    # Añadir una nueva página en el main
    daily_report_pdf.add_page(orientation="L")

    # Reading the DataFrame
    df_wtg_config = db.read_table_as_df("wtg_config", config["db"], "vis")
    df_wtg_config = df_wtg_config[
        ["id_wtg_complete", "longitude", "latitude", "id_group_complete"]
    ]   

    # Reading manual input
    dict_manual_input = read_json(
        pathlib.Path("input", "report_input", f"{DICT_WF[id_wf]}.json"),
        config['file_storage'],
        "data"
    )

    # Adding Table 1: Net Generation
    logging.info("Generating table 1")
    df_data = (
        rep.generate_test_table1_data()
        if mode_debug
        else rep.create_total_net_generation(id_wf, date_report, config)
    )
    daily_report_pdf.add_test_table1(df_data)

    # Adding Table 2: Wind Speed
    logging.info("Generating table 2")
    df_data = (
        rep.generate_test_table2_data()
        if mode_debug
        else rep.create_wind_speed_table(DICT_WF[id_wf], date_report, config)
    )
    daily_report_pdf.add_test_table2(df_data)

    # Adding Table 3: Tarif
    logging.info("Generating table 3")
    df_data = (
        rep.generate_test_table3_data()
        if mode_debug
        else rep.create_prod_oper(id_wf, date_report, config)
    )
    daily_report_pdf.add_test_table3(df_data)

    # Adding Table 4: Summary Availability
    logging.info("Generating table 4")
    df_data =  (
        rep.generate_test_table4_data()
        if mode_debug
        else rep.create_table_availability(id_wf, date_report, config)
    )        
    daily_report_pdf.add_test_table4(df_data)

    # Adding a test table 5
    logging.info("Generating table 5")
    daily_report_pdf.add_test_table5(
        dict_manual_input["Operation Maintenance and HSE highlights"])

    # Adding a test table 6
    logging.info("Generating table 6")
    daily_report_pdf.add_test_table6(
        dict_manual_input["Wind Turbines Condition Monitoring System"])

    # Adding a test table 7
    logging.info("Generating table 7")
    daily_report_pdf.add_test_table7(
        dict_manual_input["Substation & MV Underground Cable"])

    # Adding a test table 8
    logging.info("Generating table 8")
    daily_report_pdf.add_test_table8(dict_manual_input["Access Road"])

    # Adding a test table 9
    df_data = (
        rep.generate_test_table9_data()
        if mode_debug else
        rep.create_table_alarms(id_wf, date_report, config, max_alarms=8)
    )        
    logging.info("Generating table 9")
    daily_report_pdf.add_test_table9(df_data)

    # Adding a test figure
    logging.info("Generating plot")
    df_data = (
        rep.generate_test_table_plot()
        if mode_debug
        else rep.create_table_for_report_plot(id_wf, date_report, config)
    )    
    tmp_folder = pathlib.Path("data", "output", "figures")
    tmp_folder.mkdir(parents=True, exist_ok=True)
    daily_report_pdf.add_test_figure(
        df_data, 
        tmp_folder
    )

    ## Adding text
    # daily_report_pdf.cell(50, 20, "Texto de prueba")

    logging.info("Writing final PDF")
    daily_report_pdf.output(output_path)


if __name__ == "__main__":
    main(
        "Kh", # ID of the Wind Farm 
        mode_debug=True, 
        date_report=datetime(2023, 9, 24), 
        year_offset=True)
