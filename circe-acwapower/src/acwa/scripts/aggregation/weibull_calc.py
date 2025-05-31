import numpy as np
import pandas as pd
from scipy import stats
import logging
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import pytz

from acwa.data.calc.bined import classify_in_bin
from acwa.data.weibull.time_limits import define_time_limits
from acwa.config import read_config
from acwa.db import read_table_as_df, write_df_as_table
from acwa.log import format_basic_logging

def main(
        year_offset: bool = True, 
):

    """this script is thought to construct 2 tables:
    First with weibull distributions for each element (turbine, met mast) of the wind farm.
            wf_id    element_id  period  v   prob    freq    A   k

            v is windspeed bin, A is scale factor, k is shape factor. 
            period is reference to know which period of data has been study for calculation
            prob stands for fitted PDF and freq is just histogram of the data. 
    Second with just
            element_id   A   k   period
     
     """
    config = read_config()
    format_basic_logging(config["log"])
    # logging.getLogger("sqlalchemy.engine.Engine").disabled = True

    #first we shall load the data(oper_10min and oper_met_mast)
    logging.info('loading data')
    oper_10min = read_table_as_df('oper_10min', config['db'], schema='vis')
    input_met_mast = read_table_as_df('oper_met_mast', config['db'], schema='vis')
    input_met_mast = input_met_mast[input_met_mast['type'] == 'AvgValue']
    wtg_config = read_table_as_df('wtg_config',config['db'],'vis')
    
    logging.info('catching metadata')
    wtg_list=   [(wf,wtg,'WTG') for wf,wtg in zip(wtg_config['wf_name'],wtg_config['id_wtg_complete'])]
    
    mm_lst = [(wf,met_mast,'met mast') for wf,met_mast in set(zip(wtg_config['wf_name'],wtg_config['met_mast_id']))]

    element_lst = wtg_list+mm_lst
   
    logging.info('loading windspeed data')
    ws_turbine = oper_10min[['id_wtg_complete','timestamp','wind_speed']]
    ws_met_mast = input_met_mast[['met_mast_id','timestamp','wind_speed']]
    ws_met_mast.rename(columns={'met_mast_id': 'id_wtg_complete'}, inplace=True) 
    ws_total = pd.concat([ws_turbine,ws_met_mast], axis=0)
    
    utc = pytz.timezone('UTC')
    now = datetime.now(tz=utc)
    if year_offset:
        now = now - relativedelta(year=2023)

    min_time = ws_total['timestamp'].min()
    time_limits = define_time_limits(now, min_time)
    logging.info("Make timestamps timezone-aware")
    ws_total['timestamp'] = ws_total['timestamp'].dt.tz_localize('UCT', ambiguous='infer')

    row = []
    lst = []
    for dict_limits in time_limits:
        logging.info(dict_limits['period'])
        ws_period = ws_total[(ws_total['timestamp']>dict_limits['start']) & (ws_total['timestamp'] < dict_limits['end'])]
        for element in element_lst:
            wf = element[0]
            id_device = element[1]
            dev_type = element[2]
            ws_element = ws_period[ws_period['id_wtg_complete']== id_device]

            shape, scale, dist = weibull_fitting(ws_element['wind_speed'])
            
            if not(dist.empty):
                # residual = sum((dist['prob']-dist['freq'])^2)
                dist['wf_name'] = wf
                dist['id_device'] = dev_type
                dist['id_name'] = id_device
                dist['concept'] =  dict_limits['concept']
                dist['period'] = dict_limits['period']
                lst.append(dist)
            row.append({'wf_name':wf,'id_device': dev_type, 'id_name':id_device,'scale':scale,'shape':shape,'concept': dict_limits['concept'], 'period':dict_limits['period']})
    lst = [x for x in lst if not (isinstance(x, float) and np.isnan(x))]

    table1 = pd.concat(lst).reindex()
    table2 = pd.DataFrame(row)

    logging.info("Writting to table")
    write_df_as_table(
        table1,                
        config['db'],
        'vis',
        'weibull_distribution',
        index=False,
        chunksize=10000,
        if_exists = "replace"
    )
    logging.info("Writting to table")
    write_df_as_table(
        table2,                
        config['db'],
        'vis',
        'short_weibull_distribution',
        index=False,
        chunksize=10000,
        if_exists = "replace"
    )


def weibull_fitting(data):
    # Fit the Weibull distribution
    
    data = data.dropna()
    if data.empty:
        
        return np.NaN,np.NaN,pd.DataFrame()
    shape, loc, scale = stats.weibull_min.fit(data, floc=0)

    """wf_id    element_id  period  bin   prob    freq    A   k"""
    bin_width = 0.5
    data = classify_in_bin(data.to_frame(), ['wind_speed'], bin_width,mode = False)
    hist = data['wind_speed_binned'].value_counts()
    expected_values = np.arange(start = 0,stop =max(data['wind_speed_binned'])+bin_width/2,step= bin_width)
    hist = hist.reindex(expected_values, fill_value=0).reset_index().sort_values(by='wind_speed_binned')
    df = hist
    df['weibull'] = stats.weibull_min.pdf(hist['wind_speed_binned'], shape, loc, scale)
    df['freq'] = df['count']/sum(df['count'])/bin_width
    df['scale'] = scale
    df['shape'] = shape
    df = pd.melt(df,id_vars=['wind_speed_binned','count','scale','shape'], value_vars=['weibull','freq'])
    df = df.rename(columns={'variable': 'data_type'})
    
    # x = hist['wind_speed_binned']
    # # Calculate the fitted Weibull PDF
    # pdf_fitted = stats.weibull_min.pdf(x, shape, loc, scale)
    # # Plot the fitted PDF
    # plt.plot(x, pdf_fitted, 'r-', lw=2, label='Fitted Weibull PDF')

    # # Add labels and title
    # plt.xlabel('Data')
    # plt.ylabel('Density')
    # plt.title(f'Weibull Fit to Data {element}')
    # plt.legend()
    # plt.show()
    return shape, scale, df

if __name__ == "__main__":
    main()
