"""
acwa.data.datetime.format

Module to format time information
"""

from datetime import timedelta

def format_timedelta_to_HHMMSS(td: timedelta) -> str:
    """
    Format timedelta to string as HH:MM:SS

    Args:
        td (timedelta): Timedelta

    Returns:
        str: String
    """

    td_in_seconds = td.total_seconds()
    hours, remainder = divmod(td_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    if minutes < 10:
        minutes = "0{}".format(minutes)
    if seconds < 10:
        seconds = "0{}".format(seconds)
    return "{}:{}:{}".format(hours, minutes,seconds)
