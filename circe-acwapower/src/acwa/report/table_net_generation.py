"""
acwa.report.table_net_generation

Module to create the table with net generation
"""

from datetime import datetime
import pathlib

import pandas as pd

from acwa.db import read_table_as_df 
from acwa.files import read_json

def create_total_net_generation(
        id_wf: str,
        date: datetime,
        config: dict
) -> pd.DataFrame:
    """
    Create the table of total generation

    Args:
        id_wf (int): Id of wind farm
        date (datetime): Threshold date
        config (dict): Configuration

    Returns:
        pd.DataFrame: Table of total generation
    """

    # Read data
    df_wf_config = read_table_as_df("wf_config", config['db'], "vis")
    df_oper_1day = read_table_as_df("oper_1day", config['db'], "vis")

    wf_name = df_wf_config[df_wf_config['id_wf']==id_wf].iloc[0]['wf_name']
    dict_manual_input = read_json(
        pathlib.Path("input", "report_input", f"{wf_name}.json"),
        config['file_storage'],
        "data"
    )

    # Filter Wind Farm data
    df_oper_1day = df_oper_1day[df_oper_1day['id_wf']==id_wf]

    # Flag temporal info
    day_report = date.date()
    month_report = date.strftime("%Y-%B")
    year_report = date.year
    df_oper_1day['year'] = df_oper_1day['day'].dt.year
    df_oper_1day['month'] = df_oper_1day['day'].dt.strftime("%Y-%B")
    df_oper_1day['day'] = df_oper_1day['day'].dt.date

    df_oper_1day['report_day'] = df_oper_1day['day'] == day_report
    df_oper_1day['mtd'] = df_oper_1day['month'] == month_report
    df_oper_1day['ytd'] = df_oper_1day['year'] == year_report

    # Add ONEE Metering to records
    lst_records = []
    powermeter = {x: round(dict_manual_input["ONEE Metering - BusBar"][x], 2)
                  for x in ["Day", "MTD", "YTD"]}
    lst_records.append(powermeter)
    
    # Add total generation
    total_generation = {
        "Day": (df_oper_1day[df_oper_1day['report_day']]['energy'].sum() / 1000.0).round(2),
        "MTD": (df_oper_1day[df_oper_1day['mtd']]['energy'].sum() / 1000.0).round(2),
        "YTD": (df_oper_1day[df_oper_1day['ytd']]['energy'].sum() / 1000.0).round(2),
    }
    lst_records.append(total_generation)

    # Difference
    difference_perc = {
        x: f"{(total_generation[x] - powermeter[x]) / powermeter[x] * 100:.2f}%"
        for x in ["Day","MTD","YTD"]
    }
    lst_records.append(difference_perc)

    # Add P50
    budget_p50 = {
        "Day": (df_oper_1day[df_oper_1day['report_day']]['p50'].sum() / 1000.0).round(2),
        "MTD": (df_oper_1day[df_oper_1day['mtd']]['p50'].sum() / 1000.0).round(2),
        "YTD": (df_oper_1day[df_oper_1day['ytd']]['p50'].sum() / 1000.0).round(2),
    }
    lst_records.append(budget_p50)

    # Add p50 difference
    budget_p50_diff = {
        x: f"{(powermeter[x] / budget_p50[x]*100):.2f}%" 
        for x in ["Day","MTD","YTD"]
    }
    lst_records.append(budget_p50_diff)

    # Add p90
    budget_p90 = {
        "Day": (df_oper_1day[df_oper_1day['report_day']]['p90'].sum() / 1000.0).round(2),
        "MTD": (df_oper_1day[df_oper_1day['mtd']]['p90'].sum() / 1000.0).round(2),
        "YTD": (df_oper_1day[df_oper_1day['ytd']]['p90'].sum() / 1000.0).round(2),
    }
    lst_records.append(budget_p90)

    # Add p90 difference
    budget_p90_diff = {
        x: f"{(powermeter[x] / budget_p90[x]*100):.2f}%" 
        for x in ["Day","MTD","YTD"]
    }
    lst_records.append(budget_p90_diff)

    # Add PPA Brut
    ppa_brut = {x: round(dict_manual_input["Contractual Obligations PPA Brut"][x], 2)
                  for x in ["Day", "MTD", "YTD"]}
    lst_records.append(ppa_brut)

    # Add SIROCCO lower
    sirocco_lower = {x: dict_manual_input["Lower Estimation Production Forecast SIROCCO"].get(x, "-")
                  for x in ["Day", "MTD", "YTD"]}
    lst_records.append(sirocco_lower)

    # Add SIROCCO lower difference
    sirocco_lower_diff = {
        x: f"{min(powermeter[x] / sirocco_lower[x] * 100, 100):.2f}%" if sirocco_lower[x] != "-" else "-"
            for x in ["Day", "MTD", "YTD"]            
    }
    lst_records.append(sirocco_lower_diff)

    # Add SIROCCO higher
    sirocco_higher = {x: dict_manual_input["Higher Estimation Production Forecast SIROCCO"].get(x, "-")
                  for x in ["Day", "MTD", "YTD"]}
    lst_records.append(sirocco_higher)

    # Add SIROCCO higher difference
    sirocco_higher_diff = {
        x: f"{min(powermeter[x] / sirocco_higher[x] * 100, 100):.2f}%" if sirocco_higher[x] != "-" else "-"
            for x in ["Day", "MTD", "YTD"]            
    }
    lst_records.append(sirocco_higher_diff)

    # Final format
    df = pd.DataFrame.from_records(lst_records)
    df = df.round(2).astype(str)

    return df