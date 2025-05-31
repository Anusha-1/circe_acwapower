"""
acwa.data.summary.alarms

Module to summarize alarms
"""

import pandas as pd

def extract_summary_alarms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract a monthly summary of alarms

    Args:
        df (pd.DataFrame): Dataframe with treated_events_1day

    Returns:
        pd.DataFrame: Dataframe with alarms summary
    """

    # Period groups
    df["month"] = df["day"].dt.strftime("%B")
    df["year"] = df["day"].dt.strftime("%Y")

    # Alerts by month and wtg
    df_alerts_month_wtg = (
        df
        .groupby(["id_wf", "code", "id_wtg_complete", "year", "month"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["month", "total_losses"], ascending=[False, False])
        .reset_index(drop=True)
    )

    # Alerts by year and wtg
    df_alerts_year_wtg = (
        df
        .groupby(["id_wf", "code", "id_wtg_complete", "year"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values("total_losses", ascending=False)
        .reset_index(drop=True)
    )
    df_alerts_year_wtg["month"] = "All"

    # Alerts by month (complete wind farm)
    df_alerts_month_wf = (
        df
        .groupby(["id_wf", "code", "year", "month"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["month", "total_losses"], ascending=[False, False])
        .reset_index(drop=True)
    )
    df_alerts_month_wf["id_wtg_complete"] = "All"

    # Alerts by year (complete wind farm)
    df_alerts_year_wf = (
        df
        .groupby(["id_wf", "code", "year"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["total_losses"], ascending=[False])
        .reset_index(drop=True)
    )
    df_alerts_year_wf["month"] = "All"
    df_alerts_year_wf["id_wtg_complete"] = "All"

    # Alerts by general month and turbine
    df_alerts_general_month_wtg = (
        df
        .groupby(["id_wf", "code", "id_wtg_complete", "month"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["total_losses"], ascending=[False])
        .reset_index(drop=True)
    )
    df_alerts_general_month_wtg["year"] = "All"

    # Alerts by general month (complete wind farm)
    df_alerts_general_month_wf = (
        df
        .groupby(["id_wf", "code", "month"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["total_losses"], ascending=[False])
        .reset_index(drop=True)
    )
    df_alerts_general_month_wf["year"] = "All"
    df_alerts_general_month_wf["id_wtg_complete"] = "All"

    # All alerts by wtg
    df_alerts_all_wtg = (
        df
        .groupby(["id_wf", "code", "id_wtg_complete"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["total_losses"], ascending=[False])
        .reset_index(drop=True)
    )
    df_alerts_all_wtg["year"] = "All"
    df_alerts_all_wtg["month"] = "All"

    # All alerts (complete wf)
    df_alerts_all_wf = (
        df
        .groupby(["id_wf", "code"])
        .agg(total_duration=("duration", "sum"), total_losses=("losses", "sum"))
        .reset_index()
        .sort_values(["total_losses"], ascending=[False])
        .reset_index(drop=True)
    )
    df_alerts_all_wf["year"] = "All"
    df_alerts_all_wf["month"] = "All"
    df_alerts_all_wf["id_wtg_complete"] = "All"

    df_alerts = pd.concat(
        [df_alerts_month_wtg, 
         df_alerts_year_wtg, 
         df_alerts_month_wf, 
         df_alerts_year_wf,
         df_alerts_general_month_wtg,
         df_alerts_general_month_wf,
         df_alerts_all_wtg,
         df_alerts_all_wf
         ]
    )

    return df_alerts
