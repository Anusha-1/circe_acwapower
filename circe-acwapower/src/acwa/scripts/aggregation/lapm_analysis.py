"""
acwa.scripts.lapm_analysis

Script to perform the LaPM identification analysis
"""

import logging

import acwa.db as db
import acwa.lapm as lapm

from acwa.config import read_config
from acwa.log import format_basic_logging
from acwa.data import correct_speed_with_density
from acwa.tables import LapmAnalysisSchema

def main():

    config = read_config()
    format_basic_logging(config)

    logging.info("-------------- START SCRIPT: lapm_analysis -----------------")

    for data_type in ['10min', '1min']:

        logging.info(f"Working with {data_type} data")

        logging.info("Load necessary data")
        df_datapoints = db.read_table_as_df(
            f"oper_{data_type}",
            config['db'],
            "vis",
            chunksize=10000
        ) ##Repeat with 1min data

        df_sectors = db.read_table_as_df(
            "sectors",
            config['db'],
            "vis",
            chunksize=10000
        )

        logging.info("Format and clean data")
        df_datapoints = df_datapoints[df_datapoints['code']==0] ## Only running, no warnings
        df_datapoints = correct_speed_with_density(df_datapoints, dens_ref=1.09) ## Correct to fix density (HARD-CODED)
        df_datapoints = df_datapoints[['id_wtg_complete', 'timestamp', 'wind_speed_corrected', 'power', 'sector_name', 'wind_direction']].rename(
            columns={'wind_speed_corrected': 'wind_speed'}
        ) ## Keep only necessary columns
        df_datapoints = df_datapoints.dropna(subset=['wind_speed','power','wind_direction']) ## Drop NaN
        df_datapoints['wind_speed_bin'] = df_datapoints['wind_speed'].round(0) ## Bin to integers

        logging.info("Re-assign sectors")
        df_results = lapm.apply_lapm_identification_at_all_turbines(
            df_datapoints, df_sectors)
        
        logging.info("Write table")
        df_results = df_results[LapmAnalysisSchema.to_schema().columns.keys()]
        LapmAnalysisSchema.validate(df_results)
        db.write_df_as_table(
            df_results,
            config['db'],
            'vis',
            f'lapm_analysis_{data_type}',
            if_exists='replace',
            index=False,
            chunksize=10000
        )

    logging.info("----------------------- FINISH -----------------------------")

if __name__ == "__main__":
    main()
