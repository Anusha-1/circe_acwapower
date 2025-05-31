"""
acwa.reliability.index

Index of reliability models
"""

import itertools

import pandas as pd

from acwa.config import QUANTILES

def obtain_full_index_of_reliability_models(
        df_wtg_config: pd.DataFrame,
        df_temp_signals: pd.DataFrame,
        lst_signals: list[str] | None = None
) -> pd.DataFrame:
    """
    Obtain the full index of reliability models according to current 
    configuration

    Args:
        df_wtg_config (pd.DataFrame): WTG config dataframe
        df_temp_signals (pd.DataFrame): Temperature signals
        lst_signals (list[str] | None, optional): List of temperature signals to
            consider. If None, consider all. Defaults to None

    Returns:
        pd.DataFrame: Dataframe that indexes the reliability models. Columns are:
            
            - signal
            - group
            - oper_stat: "max", "min" or "median"
            - quantile  
    """

    if lst_signals is None:
        lst_signals = list(set(df_temp_signals['name_in_origin']))
    
    # Obtain set of groups
    lst_groups = list(set(df_wtg_config['id_group_complete']))
    lst_groups.sort()

    # Cartessian product of signal, group and quantile
    lst_records = []
    for signal, group, quant in itertools.product(lst_signals, lst_groups, QUANTILES.keys()):

        lst_records.append(
            {
                "signal": signal,
                "group": group,
                "oper_stat": quant,
                "quantile": QUANTILES[quant] 
            }
        )
    df = pd.DataFrame.from_records(lst_records)

    return df    
