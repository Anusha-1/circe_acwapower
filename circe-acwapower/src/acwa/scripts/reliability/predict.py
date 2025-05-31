"""
acwa.scripts.reliability.predict

Predict temperature operative ranges
"""

import logging

import pandas as pd

import acwa.data as data
import acwa.reliability as rel

from acwa.config import read_config, QUANTILES
from acwa.db import check_table, read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging


def main(incremental=True):
    config = read_config()
    format_basic_logging(config["log"])

    logging.info("----------- START SCRIPT: reliability.predict --------------")

    if not check_table("reliability_ts", config["db"], "intermediate"):
        incremental = False

    logging.info("Loading data to predict")
    df_data = data.obtain_reliability_input(
        config["db"], incremental=incremental
    )
    df_temperature_signals = read_table_as_df(
        "temperature_signals", config["db"], "vis"
    )
    lst_temp_signals = list(set(df_temperature_signals["name_in_origin"]))

    if len(df_data) == 0:
        logging.warning("No new data to predict")
        return None

    lst_groups = list(set(df_data["id_group_complete"]))
    lst_groups.sort()
    df_final_results = df_data[
        ["id_wtg_complete", "timestamp", "wind_speed", "power", "ambient_temperature"]
    ]

    for signal in lst_temp_signals:
        df_aux = data.format_features_for_reliability(df_data, signal)

        lst_df_groups = []
        for group in lst_groups:
            X, y = data.split_Xy_for_reliability(df_aux, group)
            df_group = X.copy()
            df_group["component_temperature"] = y
            cols_to_keep = ["id_wtg_complete", "timestamp", "component_temperature"]
            df_group = df_group.reset_index(drop=True) 
            # IMPORTANT! If indexes are not resetted, predictions won't appear at the correct rows 

            for quant in QUANTILES.keys():
                try:
                    logging.info(
                        f"Predicting with model for {signal} | {group} | {quant} "
                    )
                    df_group[f"{signal}_{quant}"] = rel.predict_reliability(
                        X,
                        signal,
                        group,
                        quant,
                        config["file_storage"],
                    )
                    cols_to_keep.append(f"{signal}_{quant}")
                except Exception as error:
                    logging.error(
                        f"Failing prediction for  {signal} | {group} | {quant}: {error}"
                    )

            # Corrections: Bad interpolation models and narrow distributions 
            # could result in breaking max > median > min
            df_group[f"{signal}_median"] = df_group.apply(
                lambda row: row[f"{signal}_min"] if row[f"{signal}_min"] > row[f"{signal}_median"] else row[f"{signal}_median"],
                axis = 1
            )
            df_group[f"{signal}_median"] = df_group.apply(
                lambda row: row[f"{signal}_max"] if row[f"{signal}_max"] < row[f"{signal}_median"] else row[f"{signal}_median"],
                axis = 1
            )

            df_group = df_group[cols_to_keep].rename(
                columns={"component_temperature": signal}
            )
            df_group[f"{signal}_over"] = df_group[signal] > df_group[f"{signal}_max"]
            df_group[f"{signal}_normalized"] = (
                df_group[signal] - df_group[f"{signal}_min"]
            ) / (df_group[f"{signal}_max"] - df_group[f"{signal}_min"])
            lst_df_groups.append(df_group)

        df_final_results = df_final_results.merge(
            pd.concat(lst_df_groups),
            on=["id_wtg_complete", "timestamp"],
            how="left",
        )

    logging.info("Add power group")
    df_final_results = rel.add_power_group(df_final_results, config["db"])

    logging.info("Writing predictions")
    data.write_reliability_ts(df_final_results, incremental, config["db"])

    logging.info("Writing last timestamp")
    df_final_results = df_final_results.sort_values(
        by='timestamp', ascending=False)
    df_last_results = df_final_results.drop_duplicates(
        subset=['id_wtg_complete'], keep='first')
    write_df_as_table(
        df_last_results, config['db'], "intermediate", "reliability_ts_last", 
        if_exists="replace", index=False)

if __name__ == "__main__":
    main(incremental=False)
