import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import sys

import pandas as pd
import numpy as np
import datetime

"""
This code aims to read data (csv) from Scott Cismoski, of the ARS PurpleAir hourly
PM2.5 measurements.

File naming:
    SOP: Soapstone Prairie
    BEN: Bench at Gardens on Spring Creek
    DIS: Discovery Museum
    FOS: Fossil Creek
Dataframe structure:
    column 1: location (3-digit number)
    column 2: date (mm/dd/yyyy) and time (24hr local)
    column 3: particulate type (PM2.5PA-1)
    column 4: PM2.5 measurment (AQI)
"""

def date_rename(date):
        '''Turns date strings into datetime objects.'''
        return datetime.datetime.strptime(date, r'%m/%d/%Y %H:%M')

class ARS_reader(object):    
    def __init__(self, path):
        df = pd.read_csv(path)
        
        # Add titles to the columns
        df.columns = ["Location", "Date", "Particulate", "AQI"]
        # Reset the date/times to a DateTime object
        df["Date"] = df["Date"].apply(date_rename)
        # Remove AQI less than 0 (not possible)
        df['AQI'] = df['AQI'].apply(lambda x: np.nan if (x < 0) else x)

        # Instantiate object variables
        # Allow access to DataFrame: This allows for easier processing downstream
        self.dataframe = df
        # Allow access to ndarrays for easier, short-term access
        self.date = df["Date"]
        self.location = df["Location"]
        self.aqi = df["AQI"]
        self.particulate = df["Particulate"]

def ars_read2020(date_arr):
    f_ben = '/Users/jacksontobin/Local_Documents/NightTime_Research/SQM/ARS_2020/BEN 2020 PM25.csv'
    f_sop = '/Users/jacksontobin/Local_Documents/NightTime_Research/SQM/ARS_2020/SOP 2020 PM25.csv'
    f_fos = '/Users/jacksontobin/Local_Documents/NightTime_Research/SQM/ARS_2020/FOS 2020 PM25.csv'
    f_dis = '/Users/jacksontobin/Local_Documents/NightTime_Research/SQM/ARS_2020/DIS 2020 PM25.csv'

    ben_obj = ARS_reader(f_ben)
    ben_df = ben_obj.dataframe
    sop_obj = ARS_reader(f_sop)
    sop_df = sop_obj.dataframe
    fos_obj = ARS_reader(f_fos)
    fos_df = fos_obj.dataframe
    dis_obj = ARS_reader(f_dis)
    dis_df = dis_obj.dataframe

    # Resize the DataFrames for the full year
    # date_arr = ben_df['Date']
    ben_df = ben_df.set_index('Date')
    ben_df = ben_df.reindex(date_arr)
    sop_df = sop_df.set_index('Date')
    sop_df = sop_df.reindex(date_arr)
    fos_df = fos_df.set_index('Date')
    fos_df = fos_df.reindex(date_arr)
    dis_df = dis_df.set_index('Date')
    dis_df = dis_df.reindex(date_arr)

    return ben_df, sop_df, fos_df, dis_df