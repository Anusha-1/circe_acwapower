"""
acwa.alarms.metadata.communication_loss

Add metadata for communication loss alarms
"""

MISSING_DATA_METADATA = {
    'alarm_name': '-3-Missing data',
    'code': -3,
    'description': 'Gap of missing data',
    'legacy_type': 'Custom',
    'manufacturer_availability': 'Vestas - MN',
    'operational_availability': 'NotAvailable', # Field not used
    'severity_scale': 6, # Every other real alarm will take priority over this
    'priority': 12,
    'component': 'Data Availability',
    'classification': 'Failure',
    'status': 'Failure'
}