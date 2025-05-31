"""
acwa.data.format.alarms

Format raw alarms data 
"""

import pandas as pd

from acwa.tables import InputAlarmsSchema

def map_alarms_Khalladi(df: pd.DataFrame, id_wf: int) -> pd.DataFrame:
    """
    Map input alarms data from Khalladi (i.e. rename and select columns)

    Args:
        df (pd.DataFrame): Input dataframe
        id_wf (int): Id of wind farm

    Returns:
        pd.DataFrame: Output dataframe
    """


    dict_old_to_new = {
        "Unit": "id_wtg",
        "Code": "code",
        "Description": "description",
        "Detected" : "start_datetime",
        "Reset/Run": "end_datetime",
        "Serial no.": "serial_number",
        "Event type": "event_type",
        "Severity": "severity",
        "Remark": "remark"
        }
    
    df = df[dict_old_to_new.keys()]
    df = df.rename(columns=dict_old_to_new)

    df['id_wf'] = id_wf
    df['id_wtg'] = df['id_wtg'].apply(lambda x: int(x[-2:]))
    df['id_wtg'] = df['id_wtg'].apply(lambda x: f"V0{x}" if x <10 else f"V{x}")
    df['id_wtg_complete'] = df.apply(
        lambda row: f"{row['id_wf']}-{row['id_wtg']}",
        axis=1
    )

    df['start_datetime'] = pd.to_datetime(df['start_datetime'])
    df['end_datetime'] = pd.to_datetime(df['end_datetime'])

    df = df[InputAlarmsSchema.to_schema().columns.keys()]

    return df
