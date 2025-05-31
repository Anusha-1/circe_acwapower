"""
acwa.scripts.reliability.fit_models

Script to fit Quantile Regression models to each temperature signals
"""

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging

import pandas as pd
from sklearn.metrics import mean_absolute_error

import acwa.data as data
import acwa.db as db
import acwa.reliability as rel

from acwa.config import read_config
from acwa.log import format_basic_logging


def main(
        lst_signals: list[str] | None = None,
        train_period: timedelta = timedelta(days=60),
        test_period: timedelta = timedelta(days=30),
        year_offset: bool = False):
    """
    Fit Reliability QuantileRegression models

    Args:
        lst_signals (list[str] | None, optional): List of temperature signals to
             fit. If None, fit all. Defaults to None.
        train_period (timedelta, optional): Period of data to train. 
            Defaults to timedelta(days=60).
        test_period (timedelta, optional): Period of data to test. 
            Defaults to timedelta(days=30)
        year_offset (bool, optional): If True, apply a minus 1 year to allign
            with mockup data. Defaults to False.
    """

    config = read_config()
    format_basic_logging(config["log"])

    logging.info("-------- START SCRIPT: reliability.fit_models --------------")

    logging.info("Read data")

    logging.info("Define train-test limits")
    today = datetime.now()
    if year_offset:
        today = today - relativedelta(year=2023)
    train_start = today - test_period - train_period
    train_end = today - test_period
    test_start = train_end
    test_end = today

    logging.info("Extract data to train and test")
    # This is not very efficient as we load the original table twice...
    df_data_train = data.obtain_reliability_input(
        config['db'], start_date=train_start, end_date=train_end)
    df_data_test = data.obtain_reliability_input(
        config['db'], start_date=test_start, end_date=test_end)      

    logging.info("Obtain combinations of signal, group and quantile to fit")
    df_wtg_config = db.read_table_as_df("wtg_config", config['db'], "vis")
    df_temperature_signals = db.read_table_as_df("temperature_signals", config['db'], "vis")
    df_full_index = rel.obtain_full_index_of_reliability_models(
        df_wtg_config, df_temperature_signals, lst_signals = lst_signals)
    df_full_index = rel.establish_priority(df_full_index, config['db'])
    
    for i, row in df_full_index.iterrows():

        signal = row['signal']
        group = row['group']
        oper_stat = row['oper_stat']
        quantile = row['quantile']

        ## Save initial info
        model_info = {
            'id': f'{signal}-{group}-{oper_stat}',
            'signal': signal,
            'group': group,
            'statistic': oper_stat,
            'quantile': quantile,
            'date_of_fit': today,
        }

        logging.info(f"Fitting model: {signal}-{group}-{oper_stat}")

        df_aux = data.format_features_for_reliability(
            df_data_train, signal
        )
        X, y = data.split_Xy_for_reliability(df_aux, group)

        full_model = rel.create_reliability_pipeline(quantile)
        full_model.fit(X, y)

        coef_info = rel.extract_coefficients(full_model)
        model_info = {**model_info, **coef_info}

        ## Measuring train
        df_aux['prediction_train'] = full_model.predict(X)
        df_aux_2 = df_aux[(~df_aux['prediction_train'].isna()) & (~df_aux['component_temperature'].isna())]
        mae = mean_absolute_error(
            df_aux_2['component_temperature'], df_aux_2['prediction_train'])
        model_info['start_date_train'] = train_start
        model_info['end_date_train'] = train_end
        model_info['train_mae'] = mae
        model_info['availability_at_train'] = (~df_aux['prediction_train'].isna()).mean() * 100

        ## Measuring test
        df_aux = data.format_features_for_reliability(
            df_data_test, signal
        )
        X, y = data.split_Xy_for_reliability(df_aux, group)
        df_aux['prediction_test'] = full_model.predict(X)
        df_aux_2 = df_aux[(~df_aux['prediction_test'].isna()) & (~df_aux['component_temperature'].isna())]
        mae = mean_absolute_error(
            df_aux_2['component_temperature'], df_aux_2['prediction_test'])
        model_info['start_date_test'] = test_start
        model_info['end_date_test'] = test_end
        model_info['test_mae'] = mae
        model_info['availability_at_test'] = (~df_aux['prediction_test'].isna()).mean() * 100

        logging.info(f"Saving model to pickle file for {signal} | {group} | {oper_stat}")
        rel.save_reliability_model_as_pickle(
            signal, group, oper_stat, full_model, config['file_storage']
        )
        logging.info(f"Model {signal}-{group}-{oper_stat} fitted")

        logging.info("Updating model table")
        df_full_index.at[i, "last_update"] = today
        db.write_df_as_table(
            df_full_index, config['db'], 'intermediate', 'reliability_models',
            index=False, if_exists = 'replace')
        # Note: I am assuming the table is going to be small, so we can replace
        # the entire table at each iteration, even if it is only to change one
        # row

        logging.info("Updating model metrics")
        df_metrics = pd.DataFrame.from_records([model_info])
        db.write_df_as_table(
            df_metrics, config['db'], "vis", "reliability_models_info",
            index = False, if_exists='append'
        )

if __name__ == "__main__":
    main(year_offset=True)
