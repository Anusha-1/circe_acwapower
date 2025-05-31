"""
acwa.oper.production_ratio

Module with the calculation of the production ratio
"""

import pandas as pd

def calculate_production_ratio(df_10min: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate production ratio using formula pr = power/producible

    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data, we need the columns
            'power' and 'producible'

    Returns:
        pd.DataFrame: df_10min with an extra column 'production_ratio'
    """

    def __calculate_production_ratio(row):

        if pd.isna(row['producible']):
            return None
        if pd.isna(row['power']):
            return None
        if row['producible'] <= 0:
            return 1
        
        return max(0, row['power']/row['producible'])

    df_10min["production_ratio"] = df_10min.apply(
        __calculate_production_ratio,
        axis=1
    )
    
    return df_10min
