"""
acwa.files.upload

Module to upload files to Azure
"""

import os

from azure.storage.blob import BlobClient

def upload_file(
        input_file: os.PathLike,
        output_file: os.PathLike,
        config: dict,
        container: str = None
):
    """
    Upload a file to Azure Storage account

    Args:
        input_file (os.PathLike): File in the local filesystem to upload
        output_file (os.PathLike): Destiny path in Azure Storage Account
        config (dict): Configuration of the file storage
        container (str, optional): Container in Storage Account to use. 
            Defaults to None.
    """
    
    
    with open(input_file, 'rb') as f:

        # Upload
        blob_client = BlobClient.from_connection_string(
            config['connection_string'],
            container_name=container,
            blob_name=str(output_file),
        )
    
        blob_client.upload_blob(data=f, overwrite=True)
