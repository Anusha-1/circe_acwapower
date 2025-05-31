"""
acwa.power_curves.generate

Generate power curves
"""

from datetime import datetime
import logging

import pandas as pd

from .metadata import prepare_pc_metadata_entry
from .rolling_median import create_fast_power_curve
from .wod import generate_power_curve_with_wod

def generate_power_curves(
        df: pd.DataFrame,
        df_sectors: pd.DataFrame,
        df_wtg_config: pd.DataFrame,
        start: datetime | None = None,
        end: datetime | None = None,
        concept: str | None = None,
        period: str | None = None,
        short: str | None = None,
        plot: bool = False,
        config_file: dict | None = None,
        freq: str = "10min"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate Power Curves

    Args:
        df (pd.DataFrame): 10min data
        df_pc_metadata (pd.DataFrame): Power Curve metadata
        df_sectors (pd.DataFrame): Sectors
        df_wtg_config (pd.DataFrame): WTG Config
        start (datetime | None, optional): Start of the period to consider. If 
            None, we don't limit a minimum date. Defaults to None.
        end (datetime | None, optional): End of the period to consider. If None, 
            we don't limit the maximum date. Defaults to None.
        concept (str | None, optional): Name to place in the 'concept' column at 
            metadata. Defaults to None.
        period (str | None, optional): Name to place in the 'period' column at 
            metadata. Defaults to None.
        short (str | None, optional): Initial to place in the pc_id. 
            Defaults to None.
        plot (bool, optional): Plot Power Curves. Default to False
        config_file (dict | None, optional): File Storage configuration. 
            Only needed if plot is True
        freq (str, optional): Frequency of the data. Defaults to '10min'.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            - Dataframe with PC curves
            - Dataframe with PC metadata
    """
    
    # Filter by dates
    if start is not None:
        df = df[df['timestamp'] >= start]
    if end is not None:
        df = df[df['timestamp'] <= end]

    # Filter by code (only running)
    df = df[df['code']==0]

    # Obtain combination of turbines and sectors
    df_comb = df.groupby(['id_wtg_complete','sector_name'])\
        .agg({'power': 'count'})\
        .rename(columns={'power': 'count'})\
        .reset_index()
    
    # Merge with cut-off information
    df_comb = df_comb.merge(
        df_wtg_config[['id_wtg_complete','wind_speed_stop']],
        on = 'id_wtg_complete',
        how = 'left'
    )
    
    # Loop through turbine and sector name
    df_pc = pd.DataFrame(columns=['id_wtg_complete', 'sector_name', 'bin','power','deviation'])
    lst_metadata_records = []

    for i, row in df_comb.iterrows():

        ## Isolate turbine and sector
        df_aux = df[(df['id_wtg_complete']==row['id_wtg_complete']) & (df['sector_name']==row['sector_name'])].copy()
        df_aux = df_aux[['wind_speed_corrected', 'power', 'timestamp', 'density_corrected']].rename(
            columns={
                'wind_speed_corrected': 'speed',
                'timestamp': 'datetime'
            }
        )

        ## List of densities
        lst_densities = list(set(df_aux['density_corrected']))

        for density in lst_densities:            
            try:
                logging.info(f"Generating curve for {row['id_wtg_complete']}, {row['sector_name']}, {concept}, {period}, {density}. Number of data points: {len(df_aux)}")

                ## Isolate by density
                df_aux2 = df_aux[df_aux['density_corrected']==density].copy()                                

                ## Prepare metadata
                metadata_entry = prepare_pc_metadata_entry(
                    df_sectors, row['id_wtg_complete'], row['sector_name'],
                    short, density, concept, period
                )
                lst_metadata_records.append(metadata_entry)

                ## Generate Power Curve using the WOD package
                df_pc_aux = generate_power_curve_with_wod(
                    df_aux2, 
                    name = metadata_entry['pc_id'],
                    plot=plot, config_file=config_file, freq=freq
                )
                
                ## Emergency solution (if power is zero at all values, build the curve 
                ## with a rolling median)
                if df_pc_aux['power'].sum() < 0.1:
                    logging.warning(f"Non valid curve for {metadata_entry['pc_id']}")
                    df_pc_aux = create_fast_power_curve(df_aux)

                df_pc_aux['pc_id'] = metadata_entry['pc_id']
                df_pc = pd.concat([df_pc, df_pc_aux])

                ## Filter points larger than cut-off
                df_pc = df_pc[df_pc['bin'] < row['wind_speed_stop']]
            
            except Exception as error:
                logging.error(f"Error for {row['id_wtg_complete']}, {row['sector_name']}, {concept}, {period}, {density}. Number of data points: {len(df_aux)}: {error}")

    return df_pc, pd.DataFrame.from_records(lst_metadata_records)
