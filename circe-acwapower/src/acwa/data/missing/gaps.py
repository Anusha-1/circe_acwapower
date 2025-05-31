"""
acwa.data.missing.gaps

Module to fill data gaps
"""

import pandas as pd

def fill_gaps(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Fill the missing gaps in datapoints (i.e. completely missing rows).
    These rows will be added with NaN values, and a code -3 to mark them as 
    communication loss

    Args:
        df (pd.DataFrame): Datapoints, 10min or 1min
        freq (str): Expected frequency of timestamps. Use "10min" for 10-minutes
            and "1min" for 1-minute

    Returns:
        pd.DataFrame: Dataframe with extra rows with the missing timestamps.
            Every signal will be inputted as a NaN, and a code -3
    """

    # Sort values by id_wtg_complete and datetime
    df = df.sort_values(by=['id_wtg_complete','timestamp'])\
        .reset_index(drop=True)
    
    # Create full range of datetime
    full_range = pd.date_range(
        start=df['timestamp'].min(), 
        end=df['timestamp'].max(), 
        freq=freq)
    
    # Fill the gaps for each id_wtg_complete
    new_rows = []
    for id_wtg in df['id_wtg_complete'].unique():
        df_wtg: pd.DataFrame = df[df['id_wtg_complete'] == id_wtg].copy()

        # Drop duplicates
        # We should fix this in origin...
        df_wtg = df_wtg.drop_duplicates(subset=['timestamp'], keep='first')

        # Create full range of datetime
        full_range = pd.date_range(
            start=df_wtg['timestamp'].min(), 
            end=df_wtg['timestamp'].max(), 
            freq=freq)

        full_index = pd.MultiIndex.from_product(
            [[id_wtg], full_range], names=['id_wtg_complete', 'timestamp'])
        df_wtg_full = df_wtg.set_index(
            ['id_wtg_complete', 'timestamp']).reindex(full_index).reset_index()
        new_rows.append(df_wtg_full)
    df_full = pd.concat(new_rows)

    # Mark the missing rows with a -3 code
    #df_full.loc[df_full['timestamp'].isnull(), 'code'] = -3
    df_full['code'] = df_full['code'].fillna(-3).astype('Int64')

    # Fill id_wf and id_wtg from id_wtg_complete
    df_full['id_wf'] = df_full['id_wtg_complete'].apply(
        lambda x: x.split('-')[0]
    )
    df_full['id_wtg'] = df_full['id_wtg_complete'].apply(
        lambda x: x.split('-')[1]
    )

    return df_full
