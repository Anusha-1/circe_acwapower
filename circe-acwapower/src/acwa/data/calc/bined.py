import pandas as pd
import numpy as np

def classify_in_bin(
        df:pd.DataFrame, 
        label_lst:list, 
        bin_width: float,
        df_reference: pd.DataFrame | None = None,
        mode: bool = True):

    """
    Assign bins to some lables containing numerical data

    Args:
        df (pd.DataFrame): df with variables to classify in bins
        label_lst (list): variable list wanted to be classified in bins
        bin_width (float): width of the bines
        df_reference (pd.DataFrame): Dataframe with reference data to
            decide the min and max limits
    """
    

    if df_reference is None:
        df_reference = df

    for var in label_lst:
        if mode:
            min = np.nanmin(df_reference[var])
            max = np.nanmax(df_reference[var])
        else:
            min = 0
            max = np.nanmax(df_reference[var])
        if df.empty:
            min = 0
            max = 0
        if np.isnan(max):
            max = 0
        
        bins = np.arange(
            min+bin_width/2,
            max+bin_width,
            bin_width)
        bins = np.append(min,bins) #first bin is half
        labels = np.arange(
            min,
            max+bin_width/2,
            bin_width)
        ## POSSIBLE ISSUE: What if in the new data appear a value out of range?

        df.loc[:,f'{var}_binned'] = pd.cut(
            df[var], 
            bins=bins,
            labels=labels, 
            right=False, 
            include_lowest=True).astype(float)
        df[f'{var}_binned'] = df[f'{var}_binned'].astype(float)
    
    return df

        