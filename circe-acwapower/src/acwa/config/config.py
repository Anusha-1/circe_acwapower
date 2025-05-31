"""
acwa.config.config

Module to read configuration file
"""

import pathlib

from pydantic.v1.utils import deep_update
import yaml

from acwa.cred import get_key_vault_secrets

def read_config() -> dict:
    """
    Reads config from data/main.yml

    NOTE: Update this function to include also credentials in local mode if 
    needed

    Returns:
        dict: Dictionary with configuration
    """

    # Read main default config
    path = pathlib.Path("config", "main.yml")
    with open(path, "r") as file:
        dict_config = yaml.safe_load(file)

    # Update with user specific options
    path = pathlib.Path("config", "update.yml")
    if path.exists():
        with open(path, "r") as file:
            dict_update = yaml.safe_load(file)
        dict_config = deep_update(dict_config, dict_update)

    # Update with credentials
    if dict_config['mode'] == 'local':
        path = pathlib.Path("config", "credentials.yml")
        if path.exists():
            with open(path, "r") as file:
                dict_cred = yaml.safe_load(file)            
    elif dict_config['mode'] == 'cloud':
        dict_cred = get_key_vault_secrets(dict_config['keyvault'])
    
    dict_config = deep_update(dict_config, dict_cred)

    return dict_config