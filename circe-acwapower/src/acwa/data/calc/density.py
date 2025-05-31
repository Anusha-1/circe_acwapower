"""
acwa.data.calc.density

Calculations related to air density
"""

import numpy as np
import pandas as pd

from datetime import timedelta
from acwa.db import read_table_as_df, write_df_as_table
from acwa.config import read_config


def calculate_density_10min(
    df_10min: pd.DataFrame, wtg_config: pd.DataFrame,
    df_met_mast: pd.DataFrame, met_mast_config: pd.DataFrame,
    incremental: bool = True, update_pressure: bool = True
) -> pd.DataFrame:
    """
    Calculate air density using predeterminated pressure (p_atm-rho*g*h) and
    relative humidity 75% (representative for tanger)

    Args:
        df_10min (pd.DataFrame): Dataframe with 10min data
        wtg_config (pd.DataFrame): Dataframe with turbines metadata

    Returns:
        pd.DataFrame: df_10min with densities calculated
    """
    ### estimate air pressure for each wtg
    def normalized_dens(df, temp_col:str, press_col:str, rh_col:str, density_col:str):
        
        temp_k = df[f'{temp_col}'] + 273.15 #kelvin
        press_pa = df[f"{press_col}"]*100    #Pascal
        rh = df[f'{rh_col}']/100 #/1

        r_air = 287.05  # unidades == J/(kg*K)
        r_w = 461.5  # unidades == J/(kg*K)
        p_w = 0.0000205 * np.exp(0.0631846 * temp_k)

        df[f'{density_col}'] = (1 / temp_k) * ( press_pa/ r_air  - rh * p_w * (1 / r_air - 1 / r_w))
        # obtenido de norma UNE-EN 61400-12-1 apartado 9.1.5 formula 12 : (1/T(K))*(P(Pascales)/r_air - rh*p_w*(1/r_air - 1/r_w))
        return df


    def fill_pressure(
        df: pd.DataFrame,
        pressure_column:str = 'pressure_wtg',
        rh_column:str = 'relative_humidity_mm' ,
        incremental:bool = True,
        id_col:str = 'id_wtg_complete',
        update_pressure:bool = True):
          
        
        config = read_config()
        if incremental:
            ##read old calculated mean table
            old_mean = read_table_as_df('pressure_mean_wtg', config['db'],'intermediate')

            ##ensures new df doesnt repeat timestamps (to not duplicate values when we are calculating mean)
            df = pd.merge(df, old_mean, how = 'left', on =id_col)
            df = df[df['timestamp']>df['timestamp_max']]


            df = df.drop(columns=['timestamp_max'])
            new_mean =  df.groupby(id_col)[pressure_column]\
                .agg(['mean','count'])\
                .rename(
                    columns={
                        'mean': f'{pressure_column}_mean',
                        'count': f'{pressure_column}_count'}
                    )
            new_mean[f'{pressure_column}_mean'] = new_mean[f'{pressure_column}_mean'].fillna(0) # In case of count=0
            
            ##combine both old and new mean values using wighted average
            combined = pd.merge(
                old_mean,
                new_mean, 
                how= 'left',
                on=id_col, 
                suffixes=['_x','_y']).set_index(id_col)
            new_mean[f'{pressure_column}_mean'] = (combined[f'{pressure_column}_mean_x'] * combined[f'{pressure_column}_count_x'] +combined[f'{pressure_column}_mean_y'] * combined[f'{pressure_column}_count_y']) /(combined[f'{pressure_column}_count_x'] + combined[f'{pressure_column}_count_y'])
            new_mean[f'{pressure_column}_count'] = combined[f'{pressure_column}_count_x']+combined[f'{pressure_column}_count_y']
            
            #updeates max timestamp in table
            new_mean['timestamp_max'] = df.groupby(id_col)['timestamp'].agg('max')

            df = df.drop(columns=[f'{pressure_column}_mean'])
        else:

            new_mean = df.groupby(id_col)[pressure_column]\
                .agg(['mean','count'])\
                .rename(
                    columns={
                        'mean': f'{pressure_column}_mean',
                        'count': f'{pressure_column}_count'}
                )
            new_mean['timestamp_max'] = df.groupby(id_col)['timestamp'].agg('max')

        if update_pressure:
            write_df_as_table(
                new_mean.reset_index(), 
                config=config['db'],
                schema='intermediate',
                name='pressure_mean_wtg', 
                if_exists = 'replace',
                index=False)      

        df = pd.merge(
            df,
            new_mean[f'{pressure_column}_mean'], 
            on ='id_wtg_complete', 
            how ='left')
        
        df[f'{rh_column}_mean'] = df[f'{rh_column}'].mean() #does not depend on turbine. it is not extrapolated, every turbine with met mast relative_humidity
        for var in [pressure_column,rh_column]:
            df[f'{var}_flag'] = df[var].isna()
            df[var] = df[var].fillna(df[f'{var}_mean'])
        
        return df
            

    hub_height = 80

    aux_df = pd.merge(df_10min, wtg_config[['elevation','met_mast_id','id_wtg_complete']], how='left',on='id_wtg_complete')

    aux_df = pd.merge(aux_df,met_mast_config[['met_mast_id','elevation','pres_height']].rename(columns={'elevation':'mast_elevation'}),how = 'left', on= 'met_mast_id')

    df_met_mast = df_met_mast[df_met_mast['type']=='AvgValue']
    df_met_mast = df_met_mast[['met_mast_id','timestamp','pressure','relative_humidity', 'temperature']].rename(columns={'pressure':'pressure_mm','relative_humidity':'relative_humidity_mm', 'temperature':'temperature_mm'})

    aux_df = aux_df.sort_values(by=['timestamp'])
    df_met_mast = df_met_mast.sort_values(by=['timestamp'])

    # Perform group-wise merge_asof for each id
    aux_df = pd.merge_asof(aux_df, df_met_mast, on='timestamp', by='met_mast_id', direction='forward', tolerance= timedelta(minutes=10))

    ## first task. calculating density at met mast position
    aux_df = normalized_dens(aux_df, 'temperature_mm','pressure_mm','relative_humidity_mm','density_mm')

    #Second task. Extrapolate pressures using met mast calculated density as a constant
    aux_df['pressure_wtg'] = aux_df['pressure_mm']+ aux_df['density_mm']*9.81*((aux_df['mast_elevation']+aux_df['pres_height'])-(hub_height+aux_df['elevation']))/100

    ##Here we introduce the regeneration of pressure
    aux_df = fill_pressure(
        df = aux_df, 
        pressure_column= 'pressure_wtg', 
        rh_column = 'relative_humidity_mm',  
        incremental=incremental, 
        id_col = 'id_wtg_complete',
        update_pressure = update_pressure)
 
    # Third Task. Calculate density using extrapolated pressure, turbine temperature and rh from met_mast

    aux_df = normalized_dens(aux_df, 'temperature','pressure_wtg','relative_humidity_mm', 'density_wtg')
    # aux_df.to_csv(pathlib.Path('C:\\Users\\DanielGarciaGarcia\\Desktop\\aux\\df_to_merge.csv'), index = None)


    df_10min = pd.merge(df_10min,aux_df[['id_wtg_complete','timestamp','density_wtg']], how = 'left',on=['id_wtg_complete','timestamp'])

    df_10min["density_wtg"] = df_10min["density_wtg"].map(
        lambda x: np.nan if x < 0.5 or x > 1.6  else x)
    df_10min = df_10min.rename(columns = {'density_wtg':'density'})
    return df_10min


def correct_speed_with_density(
        df: pd.DataFrame,
        dens_ref: float | str = 1.225,
        new_col_name: str = 'wind_speed_corrected'
) -> pd.DataFrame:
    """
    Apply density correction to wind speed, with the following formula:
       new_speed = speed*(dens/dens_ref)**(1/3)
    as taken from IEC 61400-12

    Args:
        df (pd.DataFrame): Data to correct
        dens_ref (float | str, optional): Reference density. If it is str, we 
            consider it as the label of the column with the reference values.
            Defaults to 1.225.
        new_col_name (str, optional): Name of new column with corrected densities. 
            Defaults to 'wind_speed_corrected'.

    Returns:
        pd.DataFrame: Dataframe with extra column
    """
    
    if isinstance(dens_ref, float):
        df[new_col_name] = df.apply(
            lambda row: row['wind_speed'] * (row['density']/dens_ref) ** (1/3),
            axis = 1
        )
    else:
        df[new_col_name] = df.apply(
            lambda row: row['wind_speed'] * (row['density']/row[dens_ref]) ** (1/3),
            axis = 1
        )

    return df

def correct_speed_with_density_auto(
        df: pd.DataFrame,
        dens_ref: list[float],
        new_col_name: str = 'wind_speed_corrected'
) -> pd.DataFrame:
    """
    Apply density correction to wind speed, with the following formula:
       new_speed = speed*(dens/dens_ref)**(1/3)
    as taken from IEC 61400-12

    Args:
        df (pd.DataFrame): Data to correct
        dens_ref (float): List of reference density.
        new_col_name (str, optional): Name of new column with corrected densities. 
            Defaults to 'wind_speed_corrected'.

    Returns:
        pd.DataFrame: Dataframe with extra column
    """

    def __correct_speed_auto(row):

        # List of distance to density
        distance = [abs(row['density'] - x) for x in dens_ref]
        zipped_list = zip(distance, dens_ref)
        min_pair = min(zipped_list, key=lambda x: x[0])
        density_for_correction = min_pair[1]

        return row['wind_speed'] * (row['density']/density_for_correction) ** (1/3)
    
    df[new_col_name] = df.apply(
        __correct_speed_auto,
        axis = 1
    )

    return df


