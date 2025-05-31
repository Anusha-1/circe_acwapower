"""
acwa.losses.distribute

Distribute losses into alarms
"""

import logging

from datetime import timedelta, datetime
from typing import Any

import numpy as np
import pandas as pd

def distribute_losses_in_alarms(
        df_alarms: pd.DataFrame,
        df_10min: pd.DataFrame,
        non_registered_alarms: bool = True,
        codes_to_ignore: list[int] | None = None
) -> pd.DataFrame:
    """
    Distribute the losses (kWh) calculated in 10-min data within the corresponding 
    alarms

    Args:
        df_alarms (pd.DataFrame): Dataframe with alarms
        df_10min (pd.DataFrame): Dataframe with 10-min data
        non_registered_alarms (bool, optional): Defaults to True
        codes_to_ignore (list[int] | None, optional): List of codes to ignore. 
            Defaults to None

    Returns:
        pd.DataFrame: Updated dataframe with alarms with extra column losses
    """
    
    list_id = list(set(df_10min['id_wtg_complete']))
    list_id.sort()
    list_dfs = []
    for i in list_id:

        logging.info(f"Turbine {i}")
        df_10min_aux = df_10min[df_10min['id_wtg_complete'] == i]
        df_alarms_aux = df_alarms[df_alarms['id_wtg_complete']==i].copy()

        if non_registered_alarms:
            df_new_alarms = extract_non_registered_alarms(df_10min_aux)
            df_alarms_aux = pd.concat([df_alarms_aux, df_new_alarms])
        
        df_alarms_aux = df_alarms_aux.sort_values(
            by='start_datetime', ascending=True)
        df_alarms_aux = df_alarms_aux.reset_index(drop=True)

        df_alarms_aux = distribute_losses_in_alarms_in_turbine(
            df_alarms_aux, df_10min_aux, codes_to_ignore=codes_to_ignore
        )
        list_dfs.append(df_alarms_aux)
    
    return pd.concat(list_dfs)

def __assign_duration_in_10min(
        row: pd.Series, start: datetime, end: datetime) -> float:
    """
    Row funtion to calculate the duration of an alarm within a 10-min segment.
    To be apply on a dataframe of alarms (axis=1)

    Args:
        row (pd.Series): Row of a dataframe of alarms. Needs to have 
            'start_datetime' and 'end_datetime'
        start (datetime): Start of the 10-min to consider
        end (datetime): End of the 10-min to consider

    Returns:
        float: Duration of the overlap between the alarm and the 10-min segment
    """

    if (start <= row['start_datetime'] < end) and (row['end_datetime'] > end):
        return (end - row['start_datetime']).total_seconds()
    
    elif (start < row['end_datetime'] <= end) and (row['start_datetime'] < start):
        return (row['end_datetime'] - start).total_seconds()
    
    elif ((start >= row['start_datetime']) and (end <= row['end_datetime'])):
        return (end-start).total_seconds()
    
    elif ((row['start_datetime'] >= start) and (row['end_datetime'] <= end)):
        return (row['end_datetime'] - row['start_datetime']).total_seconds()
    
    return None ## This shouldn't happen

def distribute_losses_in_alarms_in_turbine(
        df_alarms: pd.DataFrame,
        df_10min: pd.DataFrame,
        codes_to_ignore: list[int] | None = None
) -> pd.DataFrame:
    """
    Distribute the losses (kWh) calculated in 10-min data within the corresponding 
    alarms, at a specific turbine

    Args:
        df_alarms (pd.DataFrame): Dataframe with alarms (only one turbine)
        df_10min (pd.DataFrame): Dataframe with 10-min data (only one turbine)
        codes_to_ignore (list[int] | None, optional): List of codes to ignore. 
            Defaults to None

    Returns:
        pd.DataFrame: Updated dataframe with alarms with extra column losses
    """
    
    df_10min_aux = df_10min[df_10min['code']!=0] 
    if codes_to_ignore is not None:
        df_10min_aux = df_10min_aux[~df_10min_aux['code'].isin(codes_to_ignore)] 
    df_10min_aux = df_10min_aux.sort_values(by='timestamp', ascending=True)

    df_alarms = df_alarms.copy()
    df_alarms['losses'] = 0.0
    logging.info(f"Number of data points: {len(df_10min_aux)}")

    for i, row in df_10min_aux.iterrows():

        end_10min = row['timestamp']
        start_10min = row['timestamp'] - timedelta(minutes=10)
        loss = row['loss']
        if np.isnan(loss):
            loss = 0
        ## Inside an alarm, we might have a 10min segment without data 
        ## (i.e. loss = NaN). We put this loss as 0 so we can at least sum the 
        ## losses in the 10min with data. But we should think how we inform
        ## about this situation (maybe data availability for each alarm)

        ## Pandas Series with the start and end of the alarms
        start_alarm = df_alarms['start_datetime']
        end_alarm = df_alarms['end_datetime']

        # Take alarms occurring in that 10-min
        ## Case 1: Alarm contain the end of the 10-min  start_10min < start_alarm < end_10min <= end_alarm
        cond1 = (start_alarm < end_10min) & (end_alarm >= end_10min)
        
        ## Case 2: Alarm contain the start of the 10-min start_alarm <= start_10min < end_alarm < end_10min
        cond2 = (start_alarm <= start_10min) & (end_alarm > start_10min)
        
        ## Case 3: 10-min contains the whole alarm start_10min <= start_alarm < end_alarm <= end_10min
        cond3 = (start_alarm >= start_10min) & (end_alarm <= end_10min)
        
        ## Case 4: Alarm contain the whole 10-min start_alarm < start_10min < end_10min < end_alarm
        cond4 = (start_alarm < start_10min) & (end_alarm > end_10min)
        
        df_alarms_aux = df_alarms[cond1 | cond2 | cond3 | cond4].copy()
        
        # Add duration within the 10-min
        duration_in_10min = df_alarms_aux.apply(
            __assign_duration_in_10min, args=(start_10min, end_10min), axis=1
        )
        df_alarms_aux['duration_in_10min'] = duration_in_10min
        
        # Assign losses proportionally
        df_alarms_aux['loss'] = loss * df_alarms_aux['duration_in_10min'] / df_alarms_aux['duration_in_10min'].sum()

        # Sum losses in original dataframe
        df_alarms.loc[df_alarms_aux.index, 'losses'] += df_alarms_aux['loss'] * (1.0 / 6.0) # Transform to kWh

    return df_alarms

def extract_non_registered_alarms(df_10min: pd.DataFrame) -> pd.DataFrame:
    """
    Extract individual non-registered alarms from 10-min data

    Args:
        df_10min (pd.DataFrame): 10-min data

    Returns:
        pd.DataFrame: Dataframe with new alarms
    """

    df_10min_aux = df_10min[df_10min['code'] == -1]
    df_10min_aux = df_10min_aux.sort_values(by='timestamp', ascending=True)

    lst_records = []
    current_record = None
    for i, row in df_10min_aux.iterrows():
        
        if current_record is None:
            
            # Starting a new alarm
            current_record = create_new_non_registered_record(row)

        else:

            ## Check if the current timestamp is more than 10 minutes away.
            ## If it is, save the record and start a new one
            if (row['timestamp'] - current_record['end_datetime']) > timedelta(minutes=15):
                current_record['duration'] = int((current_record['end_datetime'] - current_record['start_datetime']).total_seconds())
                lst_records.append(current_record)
                current_record = create_new_non_registered_record(row)

            ## If not, expand the datetime
            else:
                current_record['end_datetime'] = row['timestamp']

    ## Save the last record (if any)
    if current_record is not None:
        current_record['duration'] = int((current_record['end_datetime'] - current_record['start_datetime']).total_seconds())
        lst_records.append(current_record)

    return pd.DataFrame.from_records(lst_records)

def create_new_non_registered_record(row: pd.Series) -> dict[str, Any]:
    """
    Create a new record for non-registered alarm

    Args:
        row (pd.Series): Row of a 10-min dataframe. We need 'id_wf', 'id_wtg',
            'id_wtg_complete' and 'timestamp'

    Returns:
        dict[str, Any]: Record for a new alarm
    """

    return {
        'id_wf': row['id_wf'],
        'id_wtg': row['id_wtg'],
        'id_wtg_complete': row['id_wtg_complete'],
        'code': -1,
        'description': 'Non-registered alarm',
        'component': 'Unknown',
        'start_datetime': row['timestamp'] - timedelta(minutes=10),
        'end_datetime': row['timestamp'],
        'duration': 10*60,
        'ongoing': False, # How could we treat an ongoing non-registered alarm?
        'losses': 0, # It will be calculated later,
        'time_since_previous_alarm': None, # Do we need to calculate it?
        'time_since_previous_same_alarm': None, # Do we need to calculate it?
        'serial_number': 0,
        'event_type': None,
        'severity': 0,
        'remark': None,
        'severity_scale': 1,
        'legacy_type': 'Fault',
        'classification': 'Failure',
        'manufacturer_availability': 'Vestas - MN', # Default value?
        'priority': 9 
    }
