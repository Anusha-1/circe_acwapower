"""
acwa.reliability.power_group

Add power group to reliability results
"""

import pandas as pd

from acwa.db import read_table_as_df

def add_power_group(
        df_rel_results: pd.DataFrame,
        config_db: dict
) -> pd.DataFrame:
    """
    Add power group to reliability results

    Args:
        df_rel_results (pd.DataFrame): Dataframe with reliability results
        config_db (dict): Database configuration

    Returns:
        pd.DataFrame: Dataframe with extra column 'power_group'
    """

    df_wtg_config = read_table_as_df("wtg_config", config_db, "vis")
    df_final_results = df_wtg_config[
        ["id_wtg_complete", "id_group_complete", "nominal_power"]
    ].merge(df_rel_results, how="right", on="id_wtg_complete")
    df_final_results["power_group"] = (
        df_final_results["power"] / (df_final_results["nominal_power"] / 5)
    ).apply(lambda x: round(min(5, max(0, x - 0.5) + 1)))
    df_final_results["power_group"] = df_final_results.apply(
        lambda row: f"{(row['power_group']-1)*(row['nominal_power'] / 5):.0f} - {(row['power_group'])*(row['nominal_power'] / 5):.0f} kW",
        axis=1,
    )

    return df_final_results
