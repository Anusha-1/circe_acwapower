"""
acwa.data.check_incremental

Checks incremental flag
"""

from acwa.db import check_table


def check_incremental_flag(incremental: bool, config_db: dict) -> bool:
    """
    Checks if the incremental flag is possible to be applied. We only can work
    in incremental mode if we already have results.

    Args:
        incremental (bool): Initial incremental flag
        config_db (dict): Configuration for database

    Returns:
        bool: Final incremental flag
    """

    incremental = check_table("alarms_with_losses", config_db, "intermediate") and incremental
    incremental = check_table("oper_10min", config_db, "vis") and incremental

    return incremental


def check_incremental_flag_basic(incremental: bool, config_db: dict) -> bool:
    """
    Checks if the incremental flag is possible to be applied
    (in operational_basic). We only can work in incremental mode if we already
    have results.

    Args:
        incremental (bool): Initial incremental flag
        config_db (dict): Configuration for database

    Returns:
        bool: Final incremental flag
    """

    incremental = check_table("basic_10min", config_db, "intermediate") and incremental
    incremental = check_table("basic_alarms", config_db, "intermediate") and incremental
    incremental = check_table("wind_speed_corrections", config_db, "intermediate") and incremental

    return incremental

def check_incremental_flag_1min(incremental: bool, config_db: dict) -> bool:
    """
    Checks if the incremental flag can be applied with 1min data

    Args:
        incremental (bool): Initial incremental flag
        config_db (dict): Configuration for database

    Returns:
        bool: Final incremental flag
    """

    incremental = check_table("oper_1min", config_db, "vis") and incremental

    return incremental

def check_incremental_flag_pitch(incremental: bool, config_db: dict) -> bool:
    """
    Checks if the incremental flag can be applied with pitch data

    Args:
        incremental (bool): Initial incremental flag
        config_db (dict): Configuration for database

    Returns:
        bool: Final incremental flag
    """

    incremental = check_table("pitch_with_lambda", config_db, "intermediate") and incremental

    return incremental