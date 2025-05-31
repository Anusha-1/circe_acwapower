"""
acwa.scripts.metadata.alarms

Script to upload table with alarms metadata info

FUTURE CHANGES: Adapt to multi-farm structure (issue #39)
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table
from acwa.files import read_excel
from acwa.log import format_basic_logging
from acwa.tables import AlarmsMetadataSchema
from acwa.alarms.metadata import (
    NONREGISTERED_METADATA, UNDERPERFORMING_METADATA, MISSING_DATA_METADATA)
from acwa.alarms.realtime_status import assign_status

def main():

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------- START SCRIPT: metadata.alarms ----------------")

    output_table_name = 'alarms_metadata'

    logging.info("Read Excel table")
    input_file_path = pathlib.Path('input', 'metadata', 'alarms_metadata.xlsx')
    df = read_excel(
        input_file_path,
        config['file_storage'],
        'data',
        sheet_name = 'CombinadaJun'
    )

    logging.info("Rename and format columns")
    df = df.rename(
        columns={
            "sys_logs_firstactalarmno": "code",
            "Description": "description",
            "LegacyType": "legacy_type",
            "Manufacturer Availability": "manufacturer_availability",
            "OperationalAvailability": "operational_availability",
            "Severity Scale": "severity_scale",
            "Component": "component",
            "Downtime Category": "downtime_category",
            "Priority": "priority",
            "clasificacion availability": "classification"
        }
    )
    df['component'] = df['component'].fillna("Unknown")
    df = df.drop(columns="Value")    
    df['alarm_name'] = df['code'].astype(str) + "-" + df['description']
    df['status'] = None # Just need the column defined

    logging.info("Adding custom alarms")
    df = df[AlarmsMetadataSchema.to_schema().columns.keys()]
    df = pd.concat(
        [df , 
         pd.DataFrame.from_records(
             [NONREGISTERED_METADATA, 
              UNDERPERFORMING_METADATA, 
              MISSING_DATA_METADATA])]
        )
    df['status'] = df.apply(assign_status, axis=1)

    logging.info("Write table")    
    AlarmsMetadataSchema.validate(df)
    write_df_as_table(
        df,
        config['db'],
        "vis",
        output_table_name,
        index=False,
        if_exists="replace"
    )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
