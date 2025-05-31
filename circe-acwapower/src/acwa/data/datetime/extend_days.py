"""
acwa.data.datetime.extend_days

Module to extend an alarm that crosses several days
"""

from datetime import datetime, timedelta

import pandas as pd

def extend_by_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe with priority alarms, and extend their time periods to
    to have single days (by expanding in rows)

    Args:
        df (pd.DataFrame): Dataframe with prority alarms

    Returns:
        pd.DataFrame: Expanded dataframe
    """

    lst_new_records = []

    for i, row in df.iterrows():
        start_date = row["start_datetime"].date()
        end_date = row["end_datetime"].date()

        if start_date == end_date:
            lst_new_records.append(row)

        else:
            delta = end_date - start_date
            middle_days = [
                start_date + timedelta(days=1 + i) for i in range(delta.days - 1)
            ]

            ## First day
            record = row.copy()
            end_day: datetime = start_date + timedelta(days=1)
            record["end_datetime"] = datetime(
                end_day.year, end_day.month, end_day.day, 0, 0, 0
            )
            record["duration"] = (
                record["end_datetime"] - record["start_datetime"]
            ).total_seconds()
            lst_new_records.append(record)

            ## Middle days
            for day in middle_days:
                record = row.copy()
                record["start_datetime"] = datetime(
                    day.year, day.month, day.day, 0, 0, 0
                )
                record["end_datetime"] = record["start_datetime"] + timedelta(days=1)
                record["duration"] = 24 * 60 * 60
                lst_new_records.append(record)

            ## End day
            record = row.copy()
            record["start_datetime"] = datetime(
                end_date.year, end_date.month, end_date.day, 0, 0, 0
            )
            record["duration"] = (
                record["end_datetime"] - record["start_datetime"]
            ).total_seconds()
            lst_new_records.append(record)

    return pd.DataFrame.from_records(lst_new_records)
