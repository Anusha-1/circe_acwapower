"""
acwa.power_curves.metadata

Module to prepare Power Curves metadata information
"""

from typing import Any

import pandas as pd

def prepare_pc_metadata_entry(
        df_sectors: pd.DataFrame,
        id_wtg_complete: str,
        sector: str,
        short: str,
        density: str,
        concept: str,
        period: str
) -> dict[str, Any]:
    """
    Prepare the entry in metadata to a power curve

    Args:
        df_sectors (pd.DataFrame): Dataframe with sectors
        id_wtg_complete (str): Turbine ID
        sector (str): Sector name
        short (str): Prefix for pc_id
        density (str): Density
        concept (str): Concept (Manufacturer, Historical, ...)
        period (str): Period of data taken (12 months, 6 months, ...)

    Returns:
        dict[str, Any]: Dictionary with metadata values
    """

    df_sectors_aux = df_sectors[(df_sectors['id_wtg_complete']==id_wtg_complete) & (df_sectors['sector_name']==sector)]
    main = df_sectors_aux.iloc[0]['main']
    pc_id = f"{short}_{id_wtg_complete.replace('-','_')}_{sector}_{density}"
    return {
            'pc_id': pc_id,
            'id_wtg_complete': id_wtg_complete,
            'concept': concept,
            'period': period,
            'sector_name': sector,
            'density': density,
            'main': main                
        }
                