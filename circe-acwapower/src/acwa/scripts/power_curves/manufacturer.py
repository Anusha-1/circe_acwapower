"""
acwa.scripts.power_curves.manufacturer

Script to upload manufacturer power curves. It results in two tables:

- power_curves: The power curves (bin and power)
- pc_metadata: Metadata about each power curve
"""

import logging
import pathlib

import pandas as pd

from acwa.config import read_config
from acwa.db import write_df_as_table, read_table_as_df
from acwa.files import read_file
from acwa.log import format_basic_logging
from acwa.tables import PowerCurvesSchema, PCMetadataSchema

def main():

    # Configuration and logger
    config = read_config()
    format_basic_logging(config["log"])

    logging.info("--------- START SCRIPT: power_curves.manufacturer ----------")

    logging.info("Reading power curves metadata")
    df_pc_metadata = pd.read_csv(
        read_file(
            pathlib.Path("input", "power_curves", "pc_metadata.csv"),
            config["file_storage"],
            container="data",
        )
    )
    df_pc_metadata.columns.values[0] = "pc_id"  # For some reason is misreading the first column    
    df_pc_metadata["concept"] = "Manufacturer"  # Concept: Manufacturer
    df_pc_metadata["period"] = "MN"  # Period: MN  
    df_pc_metadata['id_wtg_complete'] = df_pc_metadata.apply(
        lambda row: f"{row['id_wf']}-{row['id_wtg']}", axis=1
    )

    # Add cut-off
    df_wtg_config = read_table_as_df("wtg_config", config['db'], "vis")
    df_pc_metadata = df_pc_metadata.merge(
        df_wtg_config[['id_wtg_complete','wind_speed_stop']],
        on='id_wtg_complete',
        how='left'
    )

    logging.info("Reading original power curves")
    df_original_power_curves = pd.read_csv(
        read_file(
            pathlib.Path("input", "power_curves", "original_pc.csv"),
            config["file_storage"],
            container="data",
        )
    )

    logging.info("Reading sectors") # We need to run acwa.scripts.metadata.sectors first
    df_sectors = read_table_as_df("sectors", config['db'], "vis")

    df_pc_metadata = pd.merge(
        df_pc_metadata, 
        df_sectors[['id_wtg_complete', 'sector_name', 'main']].drop_duplicates(),
        on=['id_wtg_complete','sector_name'])
    df_power_curves = pd.merge(
        df_pc_metadata, df_original_power_curves, on=["sector_name", "density"])
    df_power_curves = df_power_curves.drop(
        columns=[
            "id_wtg_complete", "period", "sector_name", "density", "concept",
            "main", "id_wf", "id_wtg"
        ]
    )
    df_power_curves["bin"] = df_power_curves["bin"].astype(float)
    df_power_curves["power"] = df_power_curves["power"].astype(float)
    df_power_curves["sigma"] = df_power_curves["sigma"].astype(float)

    # Apply cut-off
    df_power_curves = df_power_curves[df_power_curves['bin'] <= df_power_curves["wind_speed_stop"]]
    df_pc_metadata = df_pc_metadata.drop(columns=['wind_speed_stop'])

    logging.info("Validate schemas")
    PowerCurvesSchema.validate(df_power_curves)
    df_power_curves = df_power_curves[PowerCurvesSchema.to_schema().columns.keys()]
    df_pc_metadata["density"] = df_pc_metadata["density"].astype("str")
    PCMetadataSchema.validate(df_pc_metadata)
    df_pc_metadata = df_pc_metadata[PCMetadataSchema.to_schema().columns.keys()]

    logging.info("Write tables")
    write_df_as_table(
        df_power_curves, config["db"], "vis", "power_curves",
        if_exists="replace", chunksize=10000, index=False,
    )
    write_df_as_table(
        df_pc_metadata, config["db"], "vis", "pc_metadata",
        if_exists="replace", chunksize=10000, index=False,
    )

    ## Duplicate power curves for 1min data
    write_df_as_table(
        df_power_curves, config["db"], "vis", "power_curves_1min",
        if_exists="replace", chunksize=10000, index=False,
    )
    write_df_as_table(
        df_pc_metadata, config["db"], "vis", "pc_metadata_1min",
        if_exists="replace", chunksize=10000, index=False,
    )

if __name__ == "__main__":
    main()
