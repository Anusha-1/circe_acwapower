"""
acwa.data.datetime.maintenance_limits

Module to define maintenance year limits
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

def generate_maintenance_time_limits(
        contractual_date: datetime,
        today: datetime | None = None) -> list[dict[str,datetime]]:
    """
    Divide the time period between the beginning of the contract and the current
    date into maintenance years 

    Args:
        contractual_date (datetime): Beginning of the contract
        today (datetime | None, optional): Current date. Defaults to None.

    Returns:
        list[dict[str,datetime]]: List of maintenance years. Each year is 
            defined as a dictionary, with the keys "start_date" and "end_date"
    """
    
    # Initialize the list to store time limits
    time_limits = []

    # Convert the input contractual_date (string format 'YYYY-MM-DD') to a datetime object
    start_date = contractual_date   

    # Get the current date and time
    if today is None:
        today = datetime.today()

    # Loop to create dictionary entries for each year from the contractual date till today
    while start_date < today:
        # Calculate the end date of the current year period (365 days later)
        end_date = start_date + relativedelta(years=1)

        # Add the current year period to the dictionary with the format 'yyyy.mm-dd hh:mm:ss'
        time_limits.append({
            'start_date': start_date,
            'end_date': end_date
        })

        start_date = end_date

    return time_limits
