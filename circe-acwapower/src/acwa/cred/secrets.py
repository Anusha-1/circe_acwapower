"""
acwa.cred.secrets

Module to retrieve secrets from the Key Vault
"""

from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient 


def get_key_vault_secrets(config: dict) -> dict:
    """
    Get relevant Key Vault secrets and add them to the config as credentials

    Args:
        config (dict): Configuration for the Key Vault (keyvault section)

    Returns:
        dict: Config dictionary only with the credentials
    """    

    # Identify
    credential = ManagedIdentityCredential()

    # Get a Client for the Secrets
    client = SecretClient(vault_url=config['url'],
        credential=credential)
    
    dict_credentials = {}

    ## Get SQL user
    dict_credentials['db'] = {
        "user": "dev",
        "password": client.get_secret("sql-user-dev").value
    }

    ## Get Storage Account Connection String
    dict_credentials['file_storage'] = {
        "connection_string": client.get_secret(
            "storage-account-connection-string").value
    }

    return dict_credentials
