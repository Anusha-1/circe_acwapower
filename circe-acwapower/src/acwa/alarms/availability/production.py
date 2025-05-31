"""
acwa.alarms.availability.production

Module to obtain production-based availabilities
"""

import pandas as pd

import acwa.alarms.availability.production_formulas as prod


def obtain_production_based_availabilities(
    df_10min: pd.DataFrame,
    df_alarms_metadata: pd.DataFrame,
) -> pd.DataFrame:
    """
    Obtain production-based availabilities according to norm

    Args:
        df_10min (pd.DataFrame): 10 min data
        df_alarms_metadata (pd.DataFrame): Alarms metadata

    Returns:
        pd.DataFrame: Availabilities (with actual and potential energy) per
            turbine and day
    """

    # Merge 10min with alarms metadata (we need the priority column)
    df_10min = df_10min.merge(df_alarms_metadata[["code", "priority"]], on="code")
    df_10min["day"] = df_10min["timestamp"].apply(lambda x: x.date())
    df_10min["energy"] = df_10min["power"] / 6  # transform from kw*10min to kwh
    df_10min["energy"] = df_10min["energy"].apply(lambda x: max(x, 0))
    df_10min["loss"] = df_10min["loss"] / 6

    # Obtain and merge different production-based availabilities
    df_avail = prod.obtain_production_user_I_availability(df_10min)
    df_avail_aux = prod.obtain_production_user_II_availability(df_10min)
    df_avail = df_avail.merge(df_avail_aux, on=['id_wtg_complete', 'day'])
    df_avail_aux = prod.obtain_production_manufacturer_availability(df_10min)
    df_avail = df_avail.merge(df_avail_aux, on=['id_wtg_complete', 'day'])

    return df_avail