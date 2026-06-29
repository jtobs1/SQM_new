import pandas as pd
import datetime
import numpy as np

def filter_dataframes(dataframe):
    '''
    Filters the multi-year SQM dataframe into dataframes.
    '''
    # Also remove the bad data here
    cond = (dataframe['mags'] < 0)
    dataframe['mags'] = dataframe['mags'].mask(cond, np.nan)

    dataframe['date'] = pd.to_datetime(dataframe['date'])
    
    return dataframe