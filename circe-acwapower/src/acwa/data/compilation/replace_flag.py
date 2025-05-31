"""
acwa.data.compilation.replace_flag

Determine if we need to replace during compilation
"""

import acwa.db as db

def obtain_replace_flag(
        output_table_name: str,
        config_db: dict,
        output_schema: str,
        incremental: bool,
        id: str,
        iter: int,
        data_type: str = '10min'
) -> bool:
    """
    Determine if during a wind farm iteration on the signal collection process

    Args:
        output_table_name (str): Name of the output table
        config_db (dict): Configuration of the database
        output_schema (str): Name of the output schema
        incremental (bool): Initial incremental flag
        id (str): ID of the Wind Farm or Met-Mast
        iter (int): Iteration number
        data_type (str, optional): Data type. Options are '10min', '1min', 'met_mast'. 
            Defaults to '10min'

    Returns:
        bool: Replace flag
    """

    if not incremental and iter==0:
        return True
    


    check = db.check_table(output_table_name, config_db, output_schema)
    check_wf = False
    if check and incremental:

        query_dict = {
            "10min": "select_distinct_wf",
            "1min" : "select_distinct_wf_1min",
            "met_mast": "select_distinct_met_mast"
        }

        df_existing_ids = db.run_query(
            query_dict[data_type],
            config_db,
            returns="Dataframe"
        )

        if data_type in ["10min", "1min"]:
            check_wf = id in list(df_existing_ids['id_wf'])
        elif data_type in ["met_mast"]:  
            check_wf = id in list(df_existing_ids['met_mast_id'])  

    replace_flag = True if not check_wf and iter==0 else False

    return replace_flag
