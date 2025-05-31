"""
acwa.files.read

Module to read files
"""

import json
import os
import pathlib
import pickle
from typing import TextIO, Any

from azure.storage.blob import BlobClient
import pandas as pd

def read_file(
        path: os.PathLike,
        config: dict,
        container: str = None) -> TextIO:
    """
    Read a file from path

    Args:
        path (os.PathLike): Path to file
        config (dict): Configuration of file storage (i.e. file_storage section)
        container (str): Container (only if type is Azure)

    Returns:
        (TextIO): File-like object 
    """

    if config['type'] == 'Local':

        path = pathlib.Path(
            config['root_path'],
            container,
            path
        )

        return open(path, 'r')
    
    elif config['type'] == 'Azure':        
        
        blob_client = BlobClient.from_connection_string(
            config['connection_string'],
            container_name=container,
            blob_name=str(path),
        )

        return blob_client.download_blob()
    
    else:
        raise AttributeError(
            f"Incorrect type {config['type']}. Must be 'Local' or 'Azure'")

def read_pickle(
        path: os.PathLike,
        config: dict,
        container: str = None
) -> Any:
    """
    Reads a model from a pickle file

    Args:
        path (os.PathLike): Path to file
        config (dict): Configuration of file storage (i.e. file_storage section)
        container (str): Container (only if type is Azure)

    Returns:
        Any: Object in pickle
    """

    if config['type'] == 'Local':

        path = pathlib.Path(
            config['root_path'],
            container,
            path
        )

        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj
    
    elif config['type'] == 'Azure':
        stream = read_file(path, config, container)
        return pickle.loads(stream.readall())

def read_excel(
        path: os.PathLike,
        config: dict,
        container: str = None,
        **kwargs) -> pd.DataFrame:
    """
    Read an Excel file

    Args:
        path (os.PathLike): Path to file
        config (dict): Configuration of file storage (i.e. file_storage section)
        container (str): Container (only if type is Azure)
        **kwargs: Additional kwargs for pandas.read_excel:
            https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

    Returns:
        pd.DataFrame: Dataframe from excel file
    """

    if config['type'] == 'Local':

        path = pathlib.Path(
            config['root_path'],
            container,
            path
        )

        return pd.read_excel(path, **kwargs)
    
    elif config['type'] == 'Azure':  

        blob_client = BlobClient.from_connection_string(
            config['connection_string'],
            container_name=container,
            blob_name=str(path),
        )

        downloaded_blob = blob_client.download_blob()

        return pd.read_excel(downloaded_blob.content_as_bytes(), **kwargs)

def read_json(
        path: os.PathLike,
        config: dict,
        container: str = None,) -> dict:
    """
    Read an Excel file

    Args:
        path (os.PathLike): Path to file
        config (dict): Configuration of file storage (i.e. file_storage section)
        container (str): Container (only if type is Azure)

    Returns:
        dict: Json content
    """

    if config['type'] == 'Local':

        path = pathlib.Path(
            config['root_path'],
            container,
            path
        )

        with open(path) as json_data:
            d = json.load(json_data)

        return d
    
    elif config['type'] == 'Azure':  

        blob_client = BlobClient.from_connection_string(
            config['connection_string'],
            container_name=container,
            blob_name=str(path),
        )

        downloaded_blob = blob_client.download_blob()

        return json.loads(downloaded_blob.readall())
