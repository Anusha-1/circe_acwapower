"""
acwa.alarms.custom.record

Module to define a custom alarm record
"""

from datetime import timedelta

import pandas as pd

def create_new_custom_alarm_record(row: pd.Series, dict_meta: dict) -> dict:
    """
    Create the record for a new custom alarm

    Args:
        row (pd.Series): 10min datapoint where the alarm was first detected.
        dict_meta (dict): Metadata considered for this custom alarm

    Returns:
        dict: Record for the new alarm
    """

    return {
        'id_wf': row['id_wf'],
        'id_wtg': row['id_wtg'],
        'id_wtg_complete': row['id_wtg_complete'],
        'code': dict_meta['code'],
        'description': dict_meta['description'],
        'component': dict_meta['component'],
        'start_datetime': row['timestamp'] - timedelta(minutes=10),
        'end_datetime': row['timestamp'],
        'duration': 10*60,
        'ongoing': False, # How could we treat an ongoing non-registered alarm?
        'losses': 0, # It will be calculated later,
        'time_since_previous_alarm': None, 
        'time_since_previous_same_alarm': None, 
        'serial_number': 0,
        'event_type': None,
        'severity': 0,
        'remark': None,
        'severity_scale': dict_meta['severity_scale'],
        'legacy_type': dict_meta['legacy_type'],
        'classification': dict_meta['classification'],
        'manufacturer_availability': dict_meta['manufacturer_availability'],
        'priority': dict_meta['priority'] 
    }
