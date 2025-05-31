"""
acwa.lapm.closest_sector

Module to obtain the closest LaPM sector for data points in the main sector
"""

import pandas as pd

def obtain_closest_sector(row: pd.Series, df_sectors: pd.DataFrame) -> str:
    """
    Obtain the closest LaPM sector for any datapoint

    Args:
        row (pd.Series): Datapoint
        df_sectors (pd.DataFrame): Sectors information

    Returns:
        str: Name of the closest LaPM sector
    """

    current_sector = row['sector_name']
    lapm_sectors = set(df_sectors['sector_name'])

    if current_sector in lapm_sectors:
        return current_sector
    
    direction = row['wind_direction']

    lst_distances = []
    for i, sector_row in df_sectors.iterrows():

        for boundary in ['sector_ini', 'sector_fin']:

            diff = direction - sector_row[boundary]

            if diff > 180:
                diff -= 360
            elif diff <= -180:
                diff += 360

            lst_distances.append((abs(diff), sector_row['sector_name']))

    return min(lst_distances, key = lambda t: t[0])[1]
            