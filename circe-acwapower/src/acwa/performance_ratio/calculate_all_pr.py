"""
acwa.perfromance_ration.caluclate_all_pr

Module to obtain performance ratio for all turbines and time periods
"""

import logging
from typing import Any

import pandas as pd
import numpy as np

from .integral_calc import calculate_area
from .fast_pc import calculate_fast_pc


def calculate_pr(
    df_10min: pd.DataFrame,
    pc_metadata: pd.DataFrame,
    power_curves: pd.DataFrame,
    time_limits: list[dict[str, Any]],
    wtg_lst: list[str],
    ref_dens: float,
):
    """
    Calculate Performance Ratio for a list of turbines and time periods

    Args:
        df_10min (pd.DataFrame): 10-min data
        pc_metadata (pd.DataFrame): Power Curves metadata
        power_curves (pd.DataFrame): Power Curves
        time_limits (list[dict[str, Any]]): Time periods to analyze. Include
            different metadata information
        wtg_lst (list[str]): List of WTGs to analyze
        ref_dens (float): Reference density
    """

    pr_lst = []
    df_10min = df_10min[df_10min["code"] == 0]  # running

    for period in time_limits:
        # selecting data in period to calculate PR
        df_10min_wtg = df_10min[df_10min["timestamp"] >= period["start"]].copy()
        df_10min_wtg = df_10min_wtg[df_10min_wtg["timestamp"] <= period["end"]]

        for wtg in wtg_lst:

            try:
                logging.info(
                    f"Obtaining Performance Ratio for {wtg} | {period['concept']} | {period['period']}"
                )

                delta = 0.5
                df_10min_wtg = df_10min_wtg.dropna(
                    subset=['power','wind_speed'], 
                    how='any')
                assert len(df_10min_wtg) > 0, "No valid data to calculate performance ratio"
                pc_wtg = calculate_fast_pc(
                    df_10min_wtg, delta, pd.to_numeric(ref_dens), wtg
                )

                ##extracting specific ID's of power_curves from pc_metadata
                manufact_pc_id = (
                    pc_metadata[
                        (pc_metadata["id_wtg_complete"] == wtg)
                        & (pc_metadata["main"] == 1)
                        & (pc_metadata["density"] == str(ref_dens))
                        & (pc_metadata["concept"] == "manufacturer")
                    ]
                    .reset_index()
                    .loc[0, "pc_id"]
                )
                historical_pc = pc_metadata[
                    (pc_metadata["id_wtg_complete"] == wtg)
                    & (pc_metadata["main"] == 1)
                    & (pc_metadata["density"] == str(ref_dens))
                    & (pc_metadata["concept"] == "Historical")
                    & (pc_metadata["period"] == "12 months")
                ].reset_index()
                assert not historical_pc.empty, "There is no historical power curve"
                hist_id = historical_pc.loc[0, "pc_id"]

                # calculate all areas
                area_period = np.nansum(pc_wtg["power"] * delta)
                area_manufact_pc = calculate_area(
                    power_curves,
                    manufact_pc_id,
                    pc_wtg["wind_speed_corrected_binned"].max(),
                )
                area_hist_pc = calculate_area(
                    power_curves, 
                    hist_id, 
                    pc_wtg["wind_speed_corrected_binned"].max()
                )

                # calculate PR
                pr = (
                    wtg,
                    period['concept'],
                    period["period"],
                    1 - (area_hist_pc - area_period) / area_hist_pc,
                    1 - (area_manufact_pc - area_period) / area_manufact_pc,
                )
                pr_lst.append(pr)
            except Exception as error:
                logging.error(f"Unable to obtain Performance Ratio: {error}")

    pr_df = pd.DataFrame(
        pr_lst, 
        columns=["id_wtg_complete", "concept", "period", "PR_hist", "PR_manufact"]
    )

    return pr_df
