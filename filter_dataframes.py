import pandas as pd
import datetime
import numpy as np

def filter_dataframes(dataframe):
    '''
    Filters the multi-year SQM dataframe into dataframes for each year.
    '''
    # Also remove the bad data here
    cond = (dataframe['mags'] < 0)
    dataframe['mags'] = dataframe['mags'].mask(cond, np.nan)

    dataframe['date'] = pd.to_datetime(dataframe['date'])

    df_21 = dataframe[(dataframe['date'] < datetime.datetime(year=2022,month=1,day=1))]
    df_22 = dataframe[(dataframe['date'] < datetime.datetime(year=2023,month=1,day=1)) & 
                      (dataframe['date'] > datetime.datetime(year=2022,month=1,day=1))]
    df_23 = dataframe[(dataframe['date'] > datetime.datetime(year=2023,month=1,day=1)) & 
                      (dataframe['date'] < datetime.datetime(year=2024,month=1,day=1))]
    df_24 = dataframe[(dataframe['date'] > datetime.datetime(year=2024,month=1,day=1)) & 
                      (dataframe['date'] < datetime.datetime(year=2025,month=1,day=1))]
    
    return df_21, df_22, df_23, df_24