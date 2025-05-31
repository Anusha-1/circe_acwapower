"""
acwa.config.early_detection

Parameters for early detection
"""

from datetime import timedelta

# Last period to study for reliability status
EARLY_DETECTION_PERIOD = timedelta(days=7) 

# Only study points with power > POWER_THRESHOLD x nominal_power
POWER_THRESHOLD = 0.75 

# Mark a signal as overtemperature if average of overtemp > SIGNAL_THRESHOLD
SIGNAL_THRESHOLD = 0.15 

# If a WTG has a number of affected signals > WTG_THRESHOLD, mark it as not 
# "reliable"
WTG_THRESHOLD = 0.5
