"""
acwa.report.table_report_plot

Generate table for report plot
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from acwa.db import read_table_as_df 

DICT_MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

def create_table_for_report_plot(
        id_wf: str,
        date: datetime,
        config: dict
) -> pd.DataFrame:
    """
    Create the table for the report plot

    Args:
        id_wf (str): Id of Wind Farm
        date (datetime): Date of report
        config (dict): COnfiguration

    Returns:
        pd.DataFrame: Final dataframe
    """

    # Read data
    df_oper_1day = read_table_as_df("oper_1day", config['db'], "vis")
    df_aep = read_table_as_df("AEP_table", config['db'], "vis")

    # Filter Wind Farm data
    df_oper_1day = df_oper_1day[df_oper_1day['id_wf']==id_wf]
    last_day = date + relativedelta(days=1)
    df_oper_1day = df_oper_1day[df_oper_1day['day'] < last_day]
    df_aep = df_aep[df_aep['id_wf']==id_wf]

    # Flag temporal info
    df_oper_1day['year'] = df_oper_1day['day'].dt.year
    df_oper_1day['month'] = df_oper_1day['day'].dt.strftime("%B")
    df_oper_1day['month_number'] = df_oper_1day['day'].dt.month
    df_oper_1day = df_oper_1day[df_oper_1day['year']==date.year]

    # Group by
    df_plot = df_oper_1day[['year','month', 'month_number','energy','p50', 'p90']]\
        .groupby(['year','month', 'month_number'])\
        .sum() / 1_000_000
    df_plot = df_plot.sort_values(by='month_number').reset_index().rename(
        columns={'p50': 'p50_oper', 'p90': 'p90_oper'}
    )

    # Check all month predictions
    df_aep["month"] = df_aep['timestamp'].dt.strftime("%B")
    df_aep_group = df_aep[["month","P50", "P90"]]\
        .groupby(["month"])\
        .sum()\
        .reset_index()

    # Merge
    df_total = df_aep_group.merge(
        df_plot[['month', 'energy', 'p50_oper', 'p90_oper']],
        how='left',
        on='month'
    )
    df_total['month_number'] = df_total['month'].apply(lambda x: DICT_MONTHS[x])
    df_total = df_total.sort_values(by='month_number')

    # Fill values
    current_month = date.strftime("%B")
    df_total.loc[df_total['month']==current_month, "p50_oper"] = None
    df_total.loc[df_total['month']==current_month, "p90_oper"] = None
    df_total['p50_oper'] = df_total['p50_oper'].fillna(df_total['P50'])
    df_total['p90_oper'] = df_total['p90_oper'].fillna(df_total['P90'])
    df_total['energy'] = df_total['energy'].fillna(0)

    # Subset of columns
    df_total = df_total[['month', 'energy', 'p50_oper', 'p90_oper']].rename(
        columns={"p50_oper": "P50", "p90_oper": "P90"})
    
    return df_total
