"""
acwa.data.compilation.load_info

Load mapping information
"""

import pandas as pd

import acwa.db as db

def load_mapping_information(
        config_db: dict, data_type: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads mapping and variables information

    Args:
        config_db (dict): Database configuration
        data_type (str): Data type to consider. Options are: '10min', '1min', 
            'met_mast'

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Two dataframes:

            - Mapping information
            - General variable information
    """

    df_map = db.read_table_as_df("mapping", config_db, "vis")
    df_map = df_map[df_map['data_type']==data_type]
    
    df_var = db.read_table_as_df("variables", config_db, "vis")
    df_var = df_var[df_var['data_type']==data_type]

    return df_map, df_var
