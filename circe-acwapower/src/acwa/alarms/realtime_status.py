"""
acwa.alarms.realtime_status

Module to identify real-time status
"""

import pandas as pd

def assign_status(row: pd.Series) -> str:
    """
    Assign real-time status

    Args:
        row (pd.Series): Row of dataframe with alarms info

    Returns:
        str: Status value
    """
    
    if row['priority'] in [12]:
        return "Missing data"

    if row['priority'] in [7,8,9,10,11]:
        return "Stop"
    
    if row['priority'] in [1,2,3,4,5,6]:
        
        if row['legacy_type'] == "Warning":
            return "Warning"
        
        if row['code'] == -2:
            return "Underperforming"

        return "Running"
