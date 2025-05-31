"""
acwa.reliability.save_model

Module to save reliability models
"""

from typing import Any
import logging
import pathlib
import pickle

from acwa.files import upload_file

def save_reliability_model_as_pickle(
        signal: str, group: str, oper_stat: str,
        model: Any, config_file: dict
):
    """
    Saves a reliability model to a pickle file

    Args:
        signal (str): Name of the signal
        group (str): Name of the group
        oper_stat (str): Name of the statistic
        model (Any): Object to save (i.e. the fitted model)
        config_file (dict): File storage configuration
    """
    
   

    local_path_to_model = pathlib.Path(
        "data", "output", "qr_models",
        f"{signal}_{group}_{oper_stat}.pkl"
    )
    if config_file['type'] == 'Local':
        local_path_to_model = pathlib.Path(config_file['root_path'], local_path_to_model)
    if config_file['type'] == 'Azure':
        local_path_to_model = pathlib.Path("/tmp", local_path_to_model)
    logging.info(f"Local path {local_path_to_model}")
    local_path_to_model.parent.mkdir(exist_ok=True, parents=True)
    pickle.dump(model, open(local_path_to_model, 'wb'), protocol=5)

    ## Copy to Azure if needed
    if config_file['type'] == 'Azure':

        logging.info(f"Copying model to Azure Storage account for {signal} | {group} | {oper_stat}")
        path_to_model = pathlib.Path(
            "output", "qr_models",
            f"{signal}_{group}_{oper_stat}.pkl"
        )

        upload_file(
            local_path_to_model,
            path_to_model,
            config_file,
            container='data'
        )
