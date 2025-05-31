"""
acwa.report.table_tarif.py

Module to produce table of production by tarif
"""

from datetime import datetime, timedelta

import pandas as pd

from acwa.db import read_table_as_df

def create_prod_oper(
        id_wf: int,
        date: datetime,
        config: dict
) -> pd.DataFrame:
    """
    Create the table of production by tarif

    Args:
        id_wf (int): Id of wind farm
        date (datetime): Threshold date
        config (dict): Configuration

    Returns:
        pd.DataFrame: Table of production by tarif
    """
    
    # Read the data
    df_wf_prev = read_table_as_df("oper_10min", config['db'], "vis")
    

    # Filter by wind farm id
    df_wf=df_wf_prev[df_wf_prev['id_wf'] == id_wf].copy()
    df_wf.rename(columns={'power': 'energy (mwh)'}, inplace=True)
    df_wf['energy (mwh)'] = ((1 / 6000) * df_wf['energy (mwh)']).copy()
    
    # Divide by the three tarifs
    df_first = df_wf[(df_wf['timestamp'].dt.hour >= 7) & (df_wf['timestamp'].dt.hour < 18)]
    df_second = df_wf[(df_wf['timestamp'].dt.hour >= 18) & (df_wf['timestamp'].dt.hour < 23)]
    df_third = df_wf[(df_wf['timestamp'].dt.hour >= 23) | (df_wf['timestamp'].dt.hour < 7)]

    # Aggregate values
    today = date
    mtd = today.replace(day=1,hour=0,second=0)
    ytd = today.replace(month=1, day=1,hour=0,second=0)

    energy_daily1 = df_first[(df_first['timestamp'] >= today) & (df_first['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_daily2 = df_second[(df_second['timestamp'] >= today) & (df_second['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_daily3= df_third[(df_third['timestamp'] >= today) & (df_third['timestamp'] <= today + timedelta(hours=23,minutes=50))]['energy (mwh)'].sum()
    energy_daily=energy_daily1+energy_daily2+energy_daily3
    rate1=energy_daily1/energy_daily
    rate2=energy_daily2/energy_daily
    rate3=energy_daily3/energy_daily

    energy_mtd1= df_first[(df_first['timestamp'] >= mtd) & (df_first['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_mtd2 = df_second[(df_second['timestamp'] >= mtd) & (df_second['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_mtd3= df_third[(df_third['timestamp'] >= mtd) & (df_third['timestamp'] <= today + timedelta(hours=23,minutes=50))]['energy (mwh)'].sum()
    energy_mtd=energy_mtd1+energy_mtd2+energy_mtd3
    rate1m=energy_mtd1/energy_mtd
    rate2m=energy_mtd2/energy_mtd
    rate3m=energy_mtd3/energy_mtd

    energy_ytd1= df_first[(df_first['timestamp'] >= ytd) & (df_first['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_ytd2 = df_second[(df_second['timestamp'] >= ytd) & (df_second['timestamp'] < today + timedelta(days=1))]['energy (mwh)'].sum()
    energy_ytd3= df_third[(df_third['timestamp'] >= ytd) & (df_third['timestamp'] <= today + timedelta(hours=23,minutes=50))]['energy (mwh)'].sum()
    energy_ytd=energy_ytd1+energy_ytd2+energy_ytd3
    rate1y=energy_ytd1/energy_ytd
    rate2y=energy_ytd2/energy_ytd
    rate3y=energy_ytd3/energy_ytd

    data = {
        'Period': [
            'HPL (07h - 18h)', 'Total (%)',
            'HPT (18h - 23h)', 'Total (%)',
            'HCR (23h - 07h)', 'Total (%)',
            'Total Energy Production'
        ],
        'Day': [
            energy_daily1, 100 * rate1,
            energy_daily2, 100 * rate2,
            energy_daily3, 100 * rate3,
            energy_daily
        ],
        'MTD': [
            energy_mtd1, 100 * rate1m,
            energy_mtd2, 100 * rate2m,
            energy_mtd3, 100 * rate3m,
            energy_mtd
        ],
        'YTD': [
            energy_ytd1, 100 * rate1y,
            energy_ytd2, 100 * rate2y,
            energy_ytd3, 100 * rate3y,
            energy_ytd
        ]
    }

    # Format
    energy_prod = pd.DataFrame(data)
    for column in ['Day', 'MTD', 'YTD']:
        energy_prod[column] = energy_prod[column].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x)

    return energy_prod
