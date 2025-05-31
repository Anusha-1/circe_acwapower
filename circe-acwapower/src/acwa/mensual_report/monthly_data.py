import pandas as pd 
import logging 

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from windrose import WindroseAxes
import matplotlib.cm as cm

from acwa.db import read_table_as_df
from acwa.scripts.weibull_calc import weibull_fitting
from acwa.power_curves.wod import generate_power_curve_with_wod
from acwa.power_curves.rolling_median import create_fast_power_curve

from acwa.config import read_config
from acwa.log import format_basic_logging

def to_str(number:float):
    return str(round(number,3))

def load_data(date: datetime, id_wf:str, df_lst:list, annual_mode):
    config = read_config()
    format_basic_logging(config["log"])

    logging.info('colecting necessary data for monthly report')
    new_lst = []
    if 'oper_10min' in df_lst:
        oper_10min = read_table_as_df('oper_10min', config['db'], 'vis')
        oper_10min_period = oper_10min[(oper_10min['timestamp'].dt.year == date.year) &(oper_10min['id_wf'] == id_wf)]
        if not annual_mode:
            oper_10min_period = oper_10min_period[oper_10min_period['timestamp'].dt.month == date.month]
        new_lst.append(oper_10min_period)
    if 'aep_table' in df_lst:
        aep_table = read_table_as_df('AEP_table',config['db'], 'vis')
        aep_period = aep_table[aep_table['id_wf']== id_wf]
        if not annual_mode:
            aep_period = aep_period[aep_period['timestamp'].dt.month == date.month]
        new_lst.append(aep_period)
    if 'wtg_config' in df_lst: 
        wtg_config = read_table_as_df('wtg_config',config['db'], 'vis') 
        new_lst.append(wtg_config)
    if 'oper_1day' in df_lst:
        oper_1day =read_table_as_df('oper_1day',config['db'], 'vis')
        oper_1day['day'] = pd.to_datetime(oper_1day['day'], format = '%y-%m-%d')
        oper_1day_period = oper_1day[(oper_1day['day'].dt.year == date.year) &(oper_1day['id_wf'] == id_wf)]
        if not annual_mode:
            oper_1day_period = oper_1day_period[oper_1day_period['day'].dt.month == date.month]
        new_lst.append(oper_1day_period)

    
    
    return new_lst


def get_monthly_kpi(date:datetime, id_wf:str, df_list: list):
    [oper_10min_period, aep_period, wtg_config, oper_1day] = df_list
    
    wf_production = oper_10min_period['power'].sum()/6000000
    wf_producible = oper_10min_period['historical_producible'].sum()/6000000
    total_energy_lost = wf_producible-wf_production
    wf_windspeed = oper_10min_period['wind_speed_corrected'].mean()
    wf_density = oper_10min_period['density'].mean()
    lt_density = 1.15
    availability = "operation_I"
    manufacture_availability = oper_1day[f'{availability}_available_time'].sum()/oper_1day[f'{availability}_total_time'].sum()


    p50 = aep_period['P50'].sum()
    p75 = aep_period['P75'].sum()
    p90 = aep_period['P90'].sum()
    p99 = aep_period['P99'].sum()


    lt_windspeed = wtg_config['LT_wtg'].mean()

    wf_dict = {
        'production': to_str(wf_production),
        'producible': to_str(wf_producible),
        'total_energy_lost': to_str(total_energy_lost),
        'wf_windspeed': to_str(wf_windspeed),
        'wf_density': to_str(wf_density),
        'lt_density': to_str(lt_density),
        'p50': to_str(p50),
        'p75': to_str(p75),
        'p90': to_str(p90),
        'p99': to_str(p99),
        'lt_windspeed': to_str(lt_windspeed),
        'availability': to_str(manufacture_availability*100)
    }
    return wf_dict

def get_monthly_power_wf_graph(date: datetime, id_wf: str, df_lst:list, path: pathlib.Path):
    [oper_10min_period, aep_period, wtg_config, oper_1day] = df_lst
        
    oper_1day = oper_1day[['id_wf','id_wtg', 'energy','p50']].groupby(['id_wtg','id_wf']).agg('sum').reset_index().rename(columns ={'energy': 'Produced Energy', 'p50': 'P50'})

    df_melted = oper_1day.melt(id_vars=['id_wtg'], value_vars=['Produced Energy', 'P50'], var_name='type', value_name='value') # , 'P90'
    

    sns.barplot(x = 'id_wtg', y ='value', hue = 'type',  data = df_melted,palette=["#005694","#DC267F"])
    plt.legend(loc='upper right', fontsize='medium')
    plt.title('Energy Produced vs P50', loc= 'left')
    plt.ylabel('Energy (MWh)')
    plt.xlabel(None)
    plt.xticks(rotation=90, fontsize = 8)
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()

def get_monthly_ws_wf_graph(date: datetime, id_wf: str, df_lst:list, path: pathlib.Path):
    [oper_10min_period, aep_period, wtg_config, oper_1day] = df_lst
    
    config = wtg_config.copy()
   
    oper_10min = oper_10min_period[['id_wf','id_wtg', 'wind_speed_corrected']].groupby(['id_wtg','id_wf']).agg(windspeed=('wind_speed_corrected',lambda x: x.mean())).reset_index()
    graph_table = pd.merge(oper_10min, config[['id_wf', 'id_wtg','LT_wtg']], on=['id_wf','id_wtg'], how = 'left')
    graph_table = graph_table.rename(columns= {'windspeed': 'Average Wind Speed', 'LT_wtg': 'Long Term Wind Speed'})
    df_melted = graph_table.melt(id_vars=['id_wtg','id_wf'], value_vars=['Average Wind Speed', 'Long Term Wind Speed'], var_name='type', value_name='value') # , 'P90'
                                   

    sns.barplot(x = 'id_wtg', y ='value', hue = 'type',  data = df_melted, palette=["#005694","#DC267F"])
    plt.legend(loc='upper right', fontsize='medium')
    plt.title('Month Average Wind Speed vs Long Term Wind Speed', loc= 'left')
    plt.ylabel('Wind Speed (m/s)')
    plt.xlabel(None)
    plt.xticks(rotation=90, fontsize = 8)
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()

def get_monthly_wtg_kpi(wtg:str, df_lst: list ):
    [oper_10min_period, aep_period, wtg_config, oper_1day] = df_lst
    oper_10min_period_wtg = oper_10min_period[oper_10min_period['id_wtg_complete'] == wtg]
    energy = oper_10min_period_wtg['power'].sum()/6
    producible = oper_10min_period_wtg['historical_producible'].sum()/6

def get_monthly_weibull(path,wtg_name, date, oper_10min, annual_mode):
    config = read_config()
    format_basic_logging(config["log"])
    oper_10min = oper_10min[oper_10min['timestamp'] <= date]
    df_aux = oper_10min[(oper_10min['timestamp'].dt.year == date.year) & (oper_10min['id_wtg_complete'] == wtg_name)]
    if not annual_mode:
        df_aux = df_aux[df_aux['timestamp'].dt.month == date.month]

    shape, scale, df = weibull_fitting(df_aux['wind_speed'])
    width = 8
    height = 6
    fig, ax = plt.subplots(figsize=(width, height))
    
    ## histogram
    bar_width = 0.5  # Width of each bin
    ax.bar(df[df['data_type'] == 'freq']['wind_speed_binned'], df[df['data_type'] == 'freq']['value'], width=bar_width, color="skyblue", alpha=0.7, label="Annual Data")

    # Line plot for the Weibull distribution
    ax.plot(df[df['data_type'] == 'weibull']['wind_speed_binned'], df[df['data_type'] == 'weibull']['value'], color="red", label='Weibull Distribution')
    
    plt.legend(loc='upper right', fontsize='medium')
    if annual_mode:
        plt.title(f'Annual Wind Distribution:  A = {round(scale,2)}, k = {round(shape,2)}', loc= 'left')
    else:
        plt.title(f'Monthly Wind Distribution:  A = {round(scale,2)}, k = {round(shape,2)}', loc= 'left')
    plt.ylabel('Frequency (%)')
    plt.xlabel('Wind Speed (m/s)')
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()
    return height/width

def get_historical_weibull(path,wtg_name, date, oper_10min):
    config = read_config()
    format_basic_logging(config["log"])
    
    df_aux = oper_10min[(oper_10min['timestamp'] <= date) & (oper_10min['id_wtg_complete'] == wtg_name)]
    

    shape, scale, df = weibull_fitting(df_aux['wind_speed'])
    width = 8
    height = 6
    fig, ax = plt.subplots(figsize=(width, height))
    
    ## histogram
    bar_width = 0.5  # Width of each bin
    ax.bar(df[df['data_type'] == 'freq']['wind_speed_binned'], df[df['data_type'] == 'freq']['value'], width=bar_width, color="skyblue", alpha=0.7, label="Historical Data")

    # Line plot for the Weibull distribution
    ax.plot(df[df['data_type'] == 'weibull']['wind_speed_binned'], df[df['data_type'] == 'weibull']['value'], color="red", label='Weibull Distribution')
    
    plt.legend(loc='upper right', fontsize='medium')
    plt.title(f'Accumulated Wind Distribution:  A = {round(scale,2)}, k = {round(shape,2)}', loc= 'left')
    plt.ylabel('Frequency (%)')
    plt.xlabel('Wind Speed (m/s)')
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()
    return height/width



def get_pc(path, date, pc_data, oper_10min, df_metadata, annual_mode):
    df_metadata_aux = df_metadata[df_metadata['concept'] == 'Manufacturer']
    df_10min = oper_10min[(oper_10min['timestamp'].dt.year == date.year) ]
    if not annual_mode:
        df_10min = df_10min[df_10min['timestamp'].dt.month == date.month]
    df_10min = df_10min.dropna(subset= ['timestamp','wind_speed_corrected','power','sector_name'])

    # df_pc = pc_data[pc_data['pc_id'].isin(df_metadata_aux['pc_id'])]
    df_pc = pd.merge(pc_data,df_metadata_aux[['pc_id','concept','sector_name']],on=['pc_id'], how = 'inner')

    pc_lst = [df_pc]
    for sector in set(df_10min['sector_name']):
        if sector != 'WSM':
            df_aux = df_10min[df_10min['sector_name']==sector]
            df_fpc = generate_power_curve_with_wod(df_aux[['wind_speed_corrected','power']].rename(columns={'wind_speed_corrected': 'speed'}))
            if df_fpc['power'].sum() < 0.1:
                    logging.warning(f"Non valid curve")
                    df_fpc = create_fast_power_curve(df_aux[['wind_speed_corrected','power']].rename(columns={'wind_speed_corrected': 'speed'}))
            df_fpc['pc_id'] = sector
            df_fpc['sector_name'] = sector
            df_fpc['concept'] = 'Annual'
            pc_lst.append(df_fpc)
    df_pc = pd.concat(pc_lst)
    df_pc['legend'] = df_pc['concept'] + '-'+ df_pc['sector_name']
    

    # Identify unique hue categories for scatter and line plots
    scatter_hue_types = df_10min['sector_name'].unique()
    line_hue_types = df_pc['legend'].unique()

    pastel = sns.color_palette('pastel')
    colorblind = sns.color_palette('colorblind')
    scatter_palette =(pastel[:2] +[pastel[4]] +pastel[3:])[:len(scatter_hue_types)]
    line_palette =([colorblind[0], colorblind[3],colorblind[2],colorblind[1]]+ colorblind[3:])[:len(line_hue_types)]
    width = 8
    height = 6
    fig, ax = plt.subplots(figsize=(width, height))
    plt.grid()
    #scatter power vs windspeed
    if not df_10min.empty:
        sns.scatterplot(x ='wind_speed_corrected', y = 'power', hue= 'sector_name', data = df_10min,palette=scatter_palette, ax = ax, s=10, marker = 'o', alpha = 1 )

    # Line plot for the Weibull distribution
    if not df_pc.empty:
        sns.lineplot(x = 'bin', y = 'power', hue = 'legend', data = df_pc,palette=line_palette, ax = ax )
    
    plt.gca().legend().set_title(None)
    plt.title('Power Curve', loc = 'left')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Power (kW)')
    # plt.switch_backend('TkAgg')
   
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()
  
    return height/width

def freq_wind_rose(path,date, data, annual_mode):
    df_10min = data[data['timestamp'].dt.year == date.year]
    if not annual_mode:
        df_10min = df_10min[df_10min['timestamp'].dt.month == date.month]

    df_10min = df_10min.dropna(subset=['wind_speed_corrected', 'wind_direction'])

    width = 8
    height = 6
    plt.subplots(figsize=(width, height))
    ax = WindroseAxes.from_ax()

    # Plot wind rose with 16 sectors
    if not df_10min.empty:
        ax.bar(df_10min['wind_direction'], df_10min['wind_speed_corrected'], normed=True, opening=0.8, bins=np.arange(0, 25, 5), nsector=16, cmap=sns.color_palette("mako", as_cmap = True))

    # Customize the legend
    ax.set_legend(title="Wind Speed (m/s)", loc="lower left", bbox_to_anchor=(1, 0))

    plt.title("Wind Speed Distribution and Sector Frequency")
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.close()
    return height/width
    
    
def power_wind_rose(path, date, data, annual_mode):
    df_10min = data[data['timestamp'].dt.year == date.year]
    if not annual_mode:
        df_10min = df_10min[df_10min['timestamp'].dt.month == date.month]
    df_10min = df_10min.dropna(subset=['wind_speed_corrected', 'wind_direction'])

    width = 8
    height = 6
    plt.subplots(figsize=(width, height))
    ax = WindroseAxes.from_ax()

    # Plot wind rose with 16 sectors
    if not df_10min.empty:
        ax.bar(df_10min['wind_direction'], df_10min['power'], normed=True, opening=0.8, bins=np.linspace(df_10min['power'].min(), df_10min['power'].max()*0.95, 5), nsector=16, cmap=sns.color_palette("rocket", as_cmap = True))

    # Customize the legend
    ax.set_legend(title="Power (kW)", loc="lower left", bbox_to_anchor=(1, 0))

    plt.title("Power Distribution and Sector Frequency")
    plt.savefig(path, format = 'png', dpi=300, bbox_inches='tight')
    plt.close()
    plt.close()
   
    