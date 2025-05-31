"""
acwa.report.table_availability

Module to obtain the table for summary availability
"""

from datetime import datetime

import pandas as pd

from acwa.db import read_table_as_df

def create_table_availability(
        id_wf: str,
        date: datetime,
        config: dict
) -> pd.DataFrame:
    """
    Create the table of availabilities summary

    Args:
        id_wf (int): Id of wind farm
        date (datetime): Threshold date
        config (dict): Configuration

    Returns:
        pd.DataFrame: Table of availabilities summary
    """

    # Read data
    df_man_avail = read_table_as_df(
        "manufacturer_availabilities_1day", config["db"], "vis"
    )
    df_man_avail = df_man_avail[df_man_avail['id_wf']==id_wf]

    df_oper_1day = read_table_as_df(
        "oper_1day", config["db"], "vis"
    )
    df_oper_1day = df_oper_1day[df_oper_1day['id_wf']==id_wf]

    # Flag temporal info
    day_report = date.date()
    month_report = date.strftime("%Y-%B")
    year_report = date.year
    df_man_avail['year'] = df_man_avail['day'].dt.year
    df_man_avail['month'] = df_man_avail['day'].dt.strftime("%Y-%B")
    df_man_avail['day'] = df_man_avail['day'].dt.date
    df_man_avail['Day'] = df_man_avail['day'] == day_report
    df_man_avail['MTD'] = df_man_avail['month'] == month_report
    df_man_avail['YTD'] = df_man_avail['year'] == year_report
    df_oper_1day['year'] = df_oper_1day['day'].dt.year
    df_oper_1day['month'] = df_oper_1day['day'].dt.strftime("%Y-%B")
    df_oper_1day['day'] = df_oper_1day['day'].dt.date
    df_oper_1day['Day'] = df_oper_1day['day'] == day_report
    df_oper_1day['MTD'] = df_oper_1day['month'] == month_report
    df_oper_1day['YTD'] = df_oper_1day['year'] == year_report

    # Add manufacturer downtime
    lst_records = []
    manufacturer_downtime = {
        x: df_man_avail[df_man_avail[x] & (df_man_avail['manufacturer_availability'] == 'Vestas - MN')]['duration'].sum()/3600.0
        for x in ["Day", "MTD", "YTD"]
    } 
    lst_records.append(manufacturer_downtime)

    # Add unscheduled maintenance
    unscheduled_maintenance = {
        x: df_man_avail[df_man_avail[x] & (df_man_avail['manufacturer_availability'] == 'Vestas - UM')]['duration'].sum()/3600.0
        for x in ["Day", "MTD", "YTD"]
    } 
    lst_records.append(unscheduled_maintenance)

    # Add environmental downtime
    environmental_downtime = {
        x: df_man_avail[df_man_avail[x] & (df_man_avail['manufacturer_availability'] == 'Vestas - EN')]['duration'].sum()/3600.0
        for x in ["Day", "MTD", "YTD"]
    } 
    lst_records.append(environmental_downtime)

    # Add utility downtime
    utility_downtime = {
        x: df_man_avail[df_man_avail[x] & (df_man_avail['manufacturer_availability'] == 'Vestas - UT')]['duration'].sum()/3600.0
        for x in ["Day", "MTD", "YTD"]
    } 
    lst_records.append(utility_downtime)

    ## Calculate total hours
    total_hours = {x: df_oper_1day[df_oper_1day[x]]['count_data_total'].sum() / 6.0
                   for x in ["Day", "MTD", "YTD"]}
    
    ## Calculate available hours
    available_hours = {
        x: total_hours[x] - manufacturer_downtime[x] - unscheduled_maintenance[x] - environmental_downtime[x] - utility_downtime[x]
        for x in ["Day", "MTD", "YTD"]
    }
    lst_records.append(available_hours)

    ## Percentage of Availability
    lst_records_perc = []
    perc_avail = {
        x: f"{(available_hours[x] / total_hours[x] * 100):.2f} %"
        for x in ["Day", "MTD", "YTD"]
    }
    lst_records_perc.append(perc_avail)

    ## Contractual availability
    cont_available_hours = {
        x: df_oper_1day[df_oper_1day[x]]['contractual_available_time'].sum() / 3600.0
        for x in ["Day", "MTD", "YTD"]
    }
    cont_total_hours = {
        x: df_oper_1day[df_oper_1day[x]]['contractual_total_time'].sum() / 3600.0
        for x in ["Day", "MTD", "YTD"]
    }
    cont_availability = {
        x: f"{(cont_available_hours[x] / cont_total_hours[x] * 100):.2f} %"
        for x in ["Day", "MTD", "YTD"]
    }
    lst_records_perc.append(cont_availability)

    # Final formatting
    df = pd.DataFrame.from_records(lst_records)
    df = df.round(2).astype(str)

    df = pd.concat([
        df,
        pd.DataFrame.from_records(lst_records_perc)
    ], ignore_index=True)

    # Add indices
    indices = [
        "Manufacturer Downtime (h)", "Unscheduled Maintenance (h)",
        "Environmental Downtime (h)", "Utility Downtime (h)", 
        "Wind Farm Available Hours (h)",
        "Plant Operational Availability Estimation (%)",
        "WTG Availability Calculated as per the contract (%)"]
    df['index'] = indices
    df = df.set_index("index")

    return df