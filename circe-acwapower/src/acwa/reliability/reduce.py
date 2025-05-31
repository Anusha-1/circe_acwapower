"""
acwa.reliability.reduce

Module to reduce reliability status result to a unique component
"""

import pandas as pd

def reduce_to_one_component(df: pd.DataFrame) -> pd.DataFrame:

    df_temp_melted = df.sort_values(by='signal')
    
    # Isolate the temperature of one of the signals
    df_temp_melted_repr = df_temp_melted.drop_duplicates(
        subset=['id_wtg_complete','main_component'])\
            .reset_index()[['id_wtg_complete', 'main_component', 'temperature']]
    
    # Obtain over-temperature per signals
    df_temp_melted_over = df_temp_melted.groupby(['id_wtg_complete','main_component'])\
        .agg(overtemperature = ("overtemperature", any)).reset_index()
    
    # Merge
    df_temp_final = df_temp_melted_repr.merge(
        df_temp_melted_over,
        on=['id_wtg_complete','main_component'],
        how='left'
    )

    return df_temp_final
