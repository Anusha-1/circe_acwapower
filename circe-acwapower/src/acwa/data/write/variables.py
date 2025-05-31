"""
acwa.data.write.variables

Write variables name in an independent table
"""

import pandas as pd

from acwa.config import LST_VARIABLES
from acwa.db import write_df_as_table

def write_variables_table(config_db: dict):
    """
    Write variables table

    (ONLY FOR oper_10min, FOR THE MOMENT)

    Args:
        config_db (dict): Database configuration
    """

    df = pd.DataFrame()
    df['variable_internal'] = [x[0] for x in LST_VARIABLES]
    df['variable'] = [x[1] for x in LST_VARIABLES]
    df['schema'] = 'vis'
    df['table'] = 'oper_10min'

    write_df_as_table(
        df[['schema', 'table', 'variable', 'variable_internal']], 
        config_db, "vis", "variables", if_exists="replace", index=False
    )
