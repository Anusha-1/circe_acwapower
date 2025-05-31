"""
acwa.alarms.custom.turbine

Extract custom alarms per turbine
"""

from datetime import timedelta

import pandas as pd

import acwa.alarms.metadata as am
from acwa.alarms.custom.record import create_new_custom_alarm_record

DICT_ALARM_META = {
    'Non-registered': am.NONREGISTERED_METADATA,
    'Underperforming': am.UNDERPERFORMING_METADATA,
    'Missing data': am.MISSING_DATA_METADATA
}

def extract_custom_alarms_per_turbine(
        df_10min: pd.DataFrame, custom_type: str) -> pd.DataFrame:
    """
    Extract custom alarms for a particular turbine

    Args:
        df_10min (pd.DataFrame): 10min data for a particular turbine
        custom_type (str): Type of custom alarm to extract. Options are:
            'Non-registered', 'Underperforming', 'Missing data'

    Returns:
        pd.DataFrame: Dataframe with the individual custom alarms.
    """
    
    # Filter the 10min data with the custom alarms we are looking for 
    dict_metadata = DICT_ALARM_META[custom_type]
    code = dict_metadata['code']
    df_10min_aux = df_10min[df_10min['code'] == code]
    df_10min_aux = df_10min_aux.sort_values(by='timestamp', ascending=True)

    # Loop over the 10min to save individual alarms
    lst_records = []
    current_record = None
    for i, row in df_10min_aux.iterrows():

        if current_record is None:

            # Starting a new alarm
            current_record = create_new_custom_alarm_record(row, dict_metadata)

        else:

            ## Check if the current timestamp is more than 10 minutes away.
            ## If it is, save the record and start a new one
            if (row['timestamp'] - current_record['end_datetime']) > timedelta(minutes=15):
                current_record['duration'] = int((current_record['end_datetime'] - current_record['start_datetime']).total_seconds())
                lst_records.append(current_record)
                current_record = create_new_custom_alarm_record(row, dict_metadata)

            ## If not, expand the datetime
            else:
                current_record['end_datetime'] = row['timestamp']

    ## Save the last record (if any)
    if current_record is not None:
        current_record['duration'] = int((current_record['end_datetime'] - current_record['start_datetime']).total_seconds())
        lst_records.append(current_record)

    return pd.DataFrame.from_records(lst_records)
