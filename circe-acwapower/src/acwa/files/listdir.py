"""
acwa.files.listdir

Module to list files in directory
"""

import os
import pathlib

from azure.storage.blob import BlobServiceClient

def list_files_in_path(
        path: pathlib.Path, config: dict, container: str) -> list[str]:
    """
    List all files available in path

    Args:
        path (pathlib.Path): Path to folder (inside container)
        config (dict): Configuration for data storage
        container (str): Name of container

    Raises:
        AttributeError: If type is not Local or Azure

    Returns:
        list[str]: List with files in folder
    """

    if config['type'] == 'Local':

        full_path = pathlib.Path(
            config['root_path'],
            container,
            path
        )

        return [pathlib.Path(path, x) for x in os.listdir(full_path)]
    
    elif config['type'] == 'Azure':

        blob_client = BlobServiceClient.from_connection_string(
            config['connection_string']
        )
        container_client = blob_client.get_container_client(container)
        
        return list(container_client.list_blob_names(
            name_starts_with=str(path).replace("\\","/")))

    else:
        raise AttributeError(
            f"Incorrect type {config['type']}. Must be 'Local' or 'Azure'")
