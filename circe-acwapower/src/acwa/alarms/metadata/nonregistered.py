"""
acwa.alarms.metadata.nonregistered

Add metadata for non-regesitered alarms
"""

NONREGISTERED_METADATA = {
    'alarm_name': '-1-Non-registered event',
    'code': -1,
    'description': 'Non-registered event',
    'legacy_type': 'Custom',
    'manufacturer_availability': 'Vestas - MN',
    'operational_availability': 'NotAvailable', # Field not used
    'severity_scale': 1,
    'priority': 9,
    'component': 'Unknown',
    'classification': 'Failure',
    'status': 'Failure'
}