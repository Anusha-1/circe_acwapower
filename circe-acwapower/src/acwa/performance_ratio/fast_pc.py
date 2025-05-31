
import pandas as pd
from acwa.data.calc.bined import classify_in_bin 
  
def calculate_fast_pc(
        df_oper_10min:pd.DataFrame,
        delta,
        ref_dens,
        wtg: str):

    #filter df with parameters
    
    df_10min = df_oper_10min[df_oper_10min['id_wtg_complete']== wtg].copy()
    df_10min.loc[:,'wind_speed_corrected'] = df_10min.loc[:,'wind_speed']*(df_10min.loc[:,'density']*(ref_dens))**(1/3)

    df_10min = classify_in_bin(df_10min,['wind_speed_corrected'],delta,mode= False)
    
    
    fast_pc = df_10min.groupby('wind_speed_corrected_binned',observed=False)['power'].median().reset_index()
    
    return fast_pc
