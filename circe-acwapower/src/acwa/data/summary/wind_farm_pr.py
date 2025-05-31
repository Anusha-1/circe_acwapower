"""
acwa.data.summary.wind_farm_pr

Add performance ratio to wind farm KPIs
"""

import pandas as pd

from acwa.db import read_table_as_df

def add_performance_ratio_to_kpis(
        config_db: dict,
        df_wtg_config: pd.DataFrame,
        df_oper_1day: pd.DataFrame,
        df_kpis: pd.DataFrame
) -> pd.DataFrame:
    """
    Add Performance Ratio (Manufacturer) to KPIs

    Args:
        config_db (dict): Database configuration
        df_wtg_config (pd.DataFrame): Dataframe with WTG metadata
        df_oper_1day (pd.DataFrame): Dataframe with Oper 1day results
        df_kpis (pd.DataFrame): Previous KPIs results

    Returns:
        pd.DataFrame: KPI results with extra column for performance ratio.
    """

    # Read Performance Ratio
    df_pr = read_table_as_df("performance_ratio", config_db, "vis")
    df_pr = df_pr[df_pr['concept']=='Monthly']
    df_pr = df_pr.merge(df_wtg_config[['id_wtg_complete', 'id_wf']], on='id_wtg_complete')

    # Obtain number of ok data points per turbine and period, from oper_1day
    df_oper_1day['period'] = df_oper_1day['year'] + '-' + df_oper_1day['month']
    df_turb = df_oper_1day[['id_wtg_complete', 'period', 'count_data_ok']]\
        .groupby(['id_wtg_complete', 'period']).sum()

    # Merge data, to have the number of ok data points associated to each value
    # of performance ratio
    df_pr = df_pr.merge(
        df_turb[['count_data_ok']].reset_index(),
        on=['id_wtg_complete', 'period'],
        how='left'
    )

    # Weight the performance ratio: pr_weighted = pr * count_data_ok
    df_pr['PR_manufact_weighted'] = df_pr['PR_manufact'] * df_pr['count_data_ok']

    # Group by period, to obtain the weighted average performance ratio across 
    # turbines
    df_pr_agg = df_pr[['id_wf', 'period', 'PR_manufact_weighted', 'count_data_ok']]\
        .groupby(['id_wf', 'period']).sum()
    df_pr_agg['PR_manufact'] = df_pr_agg['PR_manufact_weighted'] / df_pr_agg['count_data_ok'] * 100

    # Split year and month
    df_pr_agg = df_pr_agg.reset_index()
    df_pr_agg['year'] = df_pr_agg['period'].apply(lambda x: x.split('-')[0])
    df_pr_agg['month'] = df_pr_agg['period'].apply(lambda x: x.split('-')[1])
    
    # Aggregate per full years
    df_pr_agg_year = df_pr_agg[['id_wf', 'year', 'PR_manufact_weighted', 'count_data_ok']]\
        .groupby(['id_wf','year']).sum().reset_index()
    df_pr_agg_year['PR_manufact'] = df_pr_agg_year['PR_manufact_weighted'] / df_pr_agg_year['count_data_ok'] * 100
    df_pr_agg_year['month'] = 'All'

    # Aggregate per general months
    df_pr_agg_month = df_pr_agg[['id_wf', 'month', 'PR_manufact_weighted', 'count_data_ok']]\
        .groupby(['id_wf','month']).sum().reset_index()
    df_pr_agg_month['PR_manufact'] = df_pr_agg_month['PR_manufact_weighted'] / df_pr_agg_month['count_data_ok'] * 100
    df_pr_agg_month['year'] = 'All'

    # Aggregate full period
    df_pr_agg_all = df_pr_agg[['id_wf', 'PR_manufact_weighted', 'count_data_ok']]\
        .groupby(['id_wf']).sum().reset_index()
    df_pr_agg_all['PR_manufact'] = df_pr_agg_all['PR_manufact_weighted'] / df_pr_agg_all['count_data_ok'] * 100
    df_pr_agg_all['year'] = 'All'
    df_pr_agg_all['month'] = 'All'

    # Concatenate results
    df_pr_agg = df_pr_agg[['id_wf','year','month', 'PR_manufact']]
    df_pr_agg_year = df_pr_agg_year[['id_wf','year','month', 'PR_manufact']]
    df_pr_agg_month = df_pr_agg_month[['id_wf','year','month', 'PR_manufact']]
    df_pr_agg_all = df_pr_agg_all[['id_wf','year','month', 'PR_manufact']]
    df_pr = pd.concat([df_pr_agg, df_pr_agg_year, df_pr_agg_month, df_pr_agg_all])

    # Merge with previous KPI dataframe
    df_kpis = df_kpis.merge(
        df_pr, on=['id_wf','year','month'], how='left'
    )

    return df_kpis
