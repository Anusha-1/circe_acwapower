"""
acwa.oper.energy_availability

Module to calculate energy availability
"""

import pandas as pd

def calculate_energy_availability(df_10min: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate energy availability using the formula:

        Energy Availability = 1 - loss/(power + loss) = power / (power + loss)

    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data. Needed columns:
            'power', 'loss'

    Returns:
        pd.DataFrame: df_10min with an extra column 'energy_availability'
    """

    def __calculate_energy_availability(row):

        if pd.isna(row['loss']):
            return None
        if pd.isna(row['power']):
            return None
        if row['power'] + row['loss']  <= 0:
            return 1
        
        return max(0, row['power']/(row['power'] + row['loss']))

    df_10min["energy_availability"] = df_10min.apply(
        __calculate_energy_availability,
        axis=1
    )
    
    return df_10min
