"""
acwa.alarms.stats.mttr_mtbf.py

Module to obtain MTTR and MTBF per turbine
"""

import pandas as pd

def get_turbine_stats(df_alarms: pd.DataFrame) -> pd.DataFrame:
    """
    Get alarms duration stats (MTTR and MTBF) per turbine

    Args:
        df_alarms (pd.DataFrame): Dataframe with all the alarms

    Returns:
        pd.DataFrame: Dataframe with mttr and mtbf per turbine
    """

    df = df_alarms.groupby(['id_wtg_complete']).agg(
        {
            "duration": "mean",
            "time_since_previous_alarm": "mean"
        }
    ).reset_index().rename(columns=
        {
            "duration": "mttr",
            "time_since_previous_alarm": "mtbf"
        }
    )

    return df
