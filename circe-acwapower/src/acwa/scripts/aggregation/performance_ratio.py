

import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

import acwa.performance_ratio as perf_r

from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table 
from acwa.log import format_basic_logging

from acwa.tables import PerformanceRatioSchema

def main(
    ref_dens: float,
    wtg_lst: list | None = None,
    year_offset: bool = False):

    config = read_config()
    format_basic_logging(config['log'])

    logging.info("------------- START SCRIPT: performance_ratio --------------")

    logging.info("Load data")
    df_oper_10min = read_table_as_df("oper_10min", config['db'], "vis")
    df_oper_10min['timestamp'] = df_oper_10min['timestamp'].dt.tz_localize(
            'UCT', ambiguous='infer')
    power_curves= read_table_as_df("power_curves", config['db'], "vis")
    pc_metadata= read_table_as_df("pc_metadata", config['db'], "vis")

    if wtg_lst is None: 
        wtg_lst = sorted(set(pc_metadata['id_wtg_complete']))
        
    logging.info("Preparing time periods for power curve generation")
    now = datetime.now(tz=pytz.timezone("UTC")) + year_offset*relativedelta(year=2023)  # This will set the temporal horizons
    min_time = df_oper_10min['timestamp'].min()
    time_limits = perf_r.define_time_limits(now, min_time)  #list of dicts
    
    logging.info('Calculating performance ratio')
    pr_df = perf_r.calculate_pr(
        df_oper_10min, pc_metadata, power_curves, time_limits, wtg_lst, ref_dens)       

    logging.info("checking performance ratio schema")
    PerformanceRatioSchema.validate(pr_df)

    logging.info("Write performance ratio table")
    write_df_as_table(
        pr_df,
        config["db"],
        "vis",
        "performance_ratio",
        index=False,
        if_exists="replace",
        chunksize=10000)
 
if __name__ == "__main__":
    main(1.12, year_offset=True)

