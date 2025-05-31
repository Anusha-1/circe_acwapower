"""
acwa.data.calc.sector

Assign sector LaPM mode
"""

import pandas as pd


def create_lapm_sectors_dataframe(
        df_pc_metadata: pd.DataFrame, 
        flag_special: bool = True) -> pd.DataFrame:
    """
    Create a dataframe with the different sectors, from power curve metadata

    Args:
        df_pc_metadata (pd.DataFrame): Dataframe with power curve 
        flag_special (bool, optional): If False, return all the defined sectors; if 
            True, return only special LAPM modes. Default to False

    Returns:
        pd.DataFrame: Dataframe with individual sectors
    """

    df_sectors_lapm = df_pc_metadata[
        ["id_wtg_complete", "sector_ini", "sector_fin", "sector_name", "main"]
    ].drop_duplicates().rename(columns={'wtg': 'id_wtg'})

    if flag_special:
        df_sectors_lapm = df_sectors_lapm[
            ~((df_sectors_lapm["sector_ini"] == 0) & (df_sectors_lapm["sector_fin"] == 360))
        ]
        df_sectors_lapm = df_sectors_lapm[
            df_sectors_lapm["sector_name"].str.startswith("L")
            | df_sectors_lapm["sector_name"].str.startswith("W")
        ]
  
    return df_sectors_lapm


def assign_sector_10min(
    df: pd.DataFrame, df_sectors: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign sector operation mode in 10min data

    Args:
        df (pd.DataFrame): Dataframe with 10min data
        df_sectors (pd.DataFrame): Dataframe with individuals sectors. Necessary
            columns are: 'id_wtg', 'sector_ini', 'sector_fin', 'sector_name'

    Returns:
        pd.DataFrame: Dataframe with 10min data and an extra column
    """

    df["sector_name"] = None

    lst_id_wtg = list(set(df["id_wtg_complete"]))

    for id_wtg in lst_id_wtg:
        df_aux = df_sectors[df_sectors["id_wtg_complete"] == id_wtg].copy()

        if len(df_aux) == 1:
            df.loc[df["id_wtg_complete"] == id_wtg, "sector_name"] = list(df_aux["sector_name"])[
                0
            ]
            continue

        for i, row in df_aux.iterrows():
            if row["sector_ini"] < row["sector_fin"]:
                check = row["sector_ini"] <= df["wind_direction"]
                check = check & (df["wind_direction"] <= row["sector_fin"])
                check = check & (df["id_wtg_complete"] == id_wtg)

            else:
                check = row["sector_ini"] <= df["wind_direction"]
                check = check | (df["wind_direction"] <= row["sector_fin"])
                check = check & (df["id_wtg_complete"] == id_wtg)

            df.loc[check, "sector_name"] = row["sector_name"]

            # In case of communication loss, sector_name should be NaN
            df.loc[df['code']==-3, "sector_name"] = None

    return df


def obtain_main_sectors(df_mode: pd.DataFrame) -> pd.DataFrame:
    """
    Obtain the main 4 sectors for each turbine

    Args:
        df_mode (pd.DataFrame): Dataframe with main directions

    Returns:
        pd.DataFrame: Dataframe with main sectors
    """

    sector_records = []
    for i, row in df_mode.iterrows():
        # Main sector:
        sector_center = row["mode"]
        sector_ini = sector_center - 45.0
        if sector_ini < 0.0:
            sector_ini = 360.0 + sector_ini
        sector_fin = sector_center + 45.0
        if sector_fin >= 360.0:
            sector_fin = sector_fin - 360.0
        sector_records.append(
            {
                "id_wtg": row["id_wtg"],
                "sector_name": "Sector 1",
                "sector_ini": sector_ini,
                "sector_fin": sector_fin,
            }
        )

        # Add sectors clockwise
        for j in [2, 3, 4]:
            sector_ini = sector_fin
            if sector_ini < 0.0:
                sector_ini = 360.0 + sector_ini
            sector_fin = sector_ini + 90.0
            if sector_fin >= 360.0:
                sector_fin = sector_fin - 360.0
            sector_records.append(
                {
                    "id_wtg": row["id_wtg"],
                    "sector_name": f"Sector {j}",
                    "sector_ini": sector_ini,
                    "sector_fin": sector_fin,
                }
            )

    df_sectors = pd.DataFrame.from_records(sector_records)
    return df_sectors

def check_sectors_overlap(ini1, fin1, ini2, fin2):

    ini1 = int(ini1) + 1
    ini2 = int(ini2) + 1
    fin1 = int(fin1)
    fin2 = int(fin2)
      
    # Expandir los sectores para considerar el cruce de 0/360 grados
    sector1 = list(range(ini1, fin1 + 1)) if ini1 <= fin1 else list(range(ini1, 360)) + list(range(0, fin1 + 1))
    sector2 = list(range(ini2, fin2 + 1)) if ini2 <= fin2 else list(range(ini2, 360)) + list(range(0, fin2 + 1))
    
    # Convertir los rangos a sets para facilitar la intersección
    set1 = set(sector1)
    set2 = set(sector2)
    
    # Chequear solapamiento por intersección de sets
    overlap = not set1.isdisjoint(set2)
    return overlap

def obtain_all_sectors(
        df_mode: pd.DataFrame, 
        df_pc_metadata: pd.DataFrame) -> pd.DataFrame:
    """
    Obtain all relevant sectors combining main sectors and lapm sectors

    Args:
        df_mode (pd.DataFrame): Dataframe with main directions
        df_pc_metadata (pd.DataFrame): Dataframe with pc metadata

    Returns:
        pd.DataFrame: Dataframe with all sectors
    """

    df_regular = obtain_main_sectors(df_mode)
    df_special = create_lapm_sectors_dataframe(df_pc_metadata)


    # New dataframe
    combined_df = pd.DataFrame(columns=['id_wtg', 'sector_name', 'sector_ini', 'sector_fin'])
    
    # Iterate over id_wtg
    
    for id_wtg in df_regular['id_wtg'].unique():

        # Filter sectors for this turbine
        regular_sectors = df_regular[df_regular['id_wtg'] == id_wtg].sort_values(by='sector_ini').reset_index(drop=True)
        special_sectors = df_special[df_special['id_wtg'] == id_wtg].sort_values(by='sector_ini').reset_index(drop=True)
        
        # If there are no special sectors, just return the regular sectors
        if special_sectors.empty:
            combined_df = pd.concat([combined_df, regular_sectors])
            continue       

        # Extract all possible boundaries
        lst_boundaries = list(regular_sectors['sector_ini']) + list(special_sectors['sector_ini']) + list(special_sectors['sector_fin']) + [0,360]
        lst_boundaries.sort()
        lst_sector_segments = []
        for i in range(len(lst_boundaries) - 1):
            lst_sector_segments.append(
                {
                    "start": lst_boundaries[i],
                    "end": lst_boundaries[i+1]
                }
            )

        # Run through segments, and assign main sector
        lst_records = []
        for segment in lst_sector_segments:
            special_sector_to_add = None
            for _, row in special_sectors.iterrows():
                if check_sectors_overlap(segment['start'], segment['end'], row['sector_ini'], row['sector_fin']):
                    special_sector_to_add = row['sector_name']
                    lst_records.append(
                        {
                            "id_wtg": id_wtg,
                            "sector_name": special_sector_to_add,
                            "sector_ini": segment['start'],
                            "sector_fin": segment['end']
                        }
                    )
                    pass

            if special_sector_to_add is None:
                for _, row in regular_sectors.iterrows():
                    if check_sectors_overlap(segment['start'], segment['end'], row['sector_ini'], row['sector_fin']):
                        special_sector_to_add = row['sector_name']
                        lst_records.append(
                            {
                                "id_wtg": id_wtg,
                                "sector_name": special_sector_to_add,
                                "sector_ini": segment['start'],
                                "sector_fin": segment['end']
                            }
                        )
                        pass

            # Merge consecutive sectors if they are the same
            current_sector = lst_records[0]
            lst_merged_records = []

            for rec in lst_records[1:]:

                if current_sector['sector_name'] == rec['sector_name']:
                    current_sector['sector_fin'] = rec['sector_fin']
                else:
                    lst_merged_records.append(current_sector)
                    current_sector = rec
            
            lst_merged_records.append(current_sector)

            if lst_merged_records[0]['sector_name'] == lst_merged_records[-1]['sector_name']:
                new_sector = {
                    'id_wtg': id_wtg,
                    'sector_name': lst_merged_records[0]['sector_name'],
                    'sector_ini': lst_merged_records[-1]['sector_ini'],
                    'sector_fin': lst_merged_records[0]['sector_fin']
                }

                lst_merged_records = lst_merged_records[1:-1]
                
                lst_merged_records.append(new_sector)

        combined_df = pd.concat([combined_df, pd.DataFrame.from_records(lst_merged_records)])
    
    combined_df['id_wtg'] = combined_df['id_wtg'].astype(int)
    return combined_df
