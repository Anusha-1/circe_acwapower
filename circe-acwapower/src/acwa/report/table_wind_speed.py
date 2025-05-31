"""
acwa.report.table_wind_speed

Module to create table with environmental report
"""

from datetime import datetime, timedelta

import pandas as pd

from acwa.db import read_table_as_df

def create_wind_speed_table(
        wf_name: str,
        date: datetime,
        config: dict
) -> pd.DataFrame:
    """
    Create wind speed table 

    Args:
        wf_name (str): Name of the wind farm
        date (datetime): Threshold date
        config (dict): Configuration

    Returns:
        pd.DataFrame: Table with environmental conditions
    """

    # Read data
    df_wf_prev = read_table_as_df("oper_met_mast", config['db'], "vis")

    # Filter by wind farm name
    df_wf=df_wf_prev[df_wf_prev['wf_name'] == wf_name]

    #Filter by requested metric
    avg_velocities = df_wf[df_wf['type'] == 'AvgValue']
    max_velocities = df_wf[df_wf['type'] == 'MaxValue']
    min_velocities = df_wf[df_wf['type'] == 'MinValue']

    #Date assignment
    today=date

    #Data treatment by day
    daily_data_avg = avg_velocities[(avg_velocities['timestamp'] >= today - timedelta(days=1)) & (avg_velocities['timestamp'] <=today)]['wind_speed'].mean()
    daily_data_max = max_velocities[(max_velocities['timestamp'] >= today - timedelta(days=1)) & (max_velocities['timestamp'] <=today)]['wind_speed'].max()
    daily_data_min = min_velocities[(min_velocities['timestamp'] >= today - timedelta(days=1)) & (min_velocities['timestamp'] <=today)]['wind_speed'].min()
    daily_data_temperature = avg_velocities[(avg_velocities['timestamp'] >= today - timedelta(days=1)) & (avg_velocities['timestamp'] < today)]['temperature'].mean()

    # By MTD
    mtd = today.replace(day=1,hour=0,second=0)

    mtd_data_avg = avg_velocities[(avg_velocities['timestamp']>= mtd) & (avg_velocities['timestamp'] <=today)]['wind_speed'].mean()
    mtd_data_max = max_velocities[(max_velocities['timestamp']>= mtd) & (max_velocities['timestamp'] <=today)]['wind_speed'].max()
    mtd_data_min = min_velocities[(min_velocities['timestamp']>= mtd) & (min_velocities['timestamp'] <=today)]['wind_speed'].min()
    mtd_data_temperature = avg_velocities[(avg_velocities['timestamp'] >= mtd) & (avg_velocities['timestamp'] <= today)]['wind_speed'].mean()

    # By YTD
    ytd = today.replace(month=1, day=1,hour=0,second=0)


    ytd_data_avg = avg_velocities[(avg_velocities['timestamp']>= ytd) & (avg_velocities['timestamp'] <=today)]['wind_speed'].mean()
    ytd_data_max = max_velocities[(max_velocities['timestamp']>= ytd) & (max_velocities['timestamp'] <= today)]['wind_speed'].max()
    ytd_data_min = min_velocities[(min_velocities['timestamp']>= ytd) & (min_velocities['timestamp'] <=today)]['wind_speed'].min()
    ytd_data_temperature=avg_velocities[(avg_velocities['timestamp'] >= ytd) & (avg_velocities['timestamp'] <= today)]['temperature'].mean()



    
    # Format final data
    data = {
    "Metric": [
        "Wind Speed Average (m/s)", "Wind Speed Min (m/s)", "Wind Speed Max (m/s)",
        "Ambient Temperature Average (ºC)"
    ],
    "Day": [daily_data_avg, daily_data_min, daily_data_max,daily_data_temperature ],
    "MTD": [mtd_data_avg, mtd_data_min, mtd_data_max, mtd_data_temperature],
    "YTD": [ytd_data_avg, ytd_data_min, ytd_data_max,ytd_data_temperature]
    }

    wind_table = pd.DataFrame(data)
    wind_table['Day'] = wind_table['Day'].round(2).astype(str)
    wind_table['MTD'] = wind_table['MTD'].round(2).astype(str)
    wind_table['YTD'] = wind_table['YTD'].round(2).astype(str)
    
    return wind_table
