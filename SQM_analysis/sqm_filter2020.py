import sqm_read2020
import sqm_plot2020
import ars_read2020
import numpy as np
import pandas as pd
import sys

fname = '/Users/jacksontobin/Local_Documents/NightTime_Research/FoCo Night Sky Team/Fort Collins SQM Monitoring 2020/Fort Collins SQM 2020 data(all_sites_copy2).csv'

# Read the data without filtering the lunar phase or cloud cover
dataframes = sqm_read2020.read_2020(fname=fname, filter_phase=False, filter_cloud=False)

# Read the ARS data 
date_arr = dataframes[0].index
df_ben, df_sop, df_fos, df_dis = ars_read2020.ars_read2020(date_arr=date_arr)

# Now we can plot the data by filtering out each lunar phase and cloud cover
# Let's just look at one location:
# 0: FRNA (HZ), 1: FRNA (ZN), 2: FCMOD, 3: PFA1, 4: PFA2, 5: HILT, 6: SPZN, 7: SPHZ
loc = 2
df_fcmod = dataframes[loc]
print(df_fcmod.head())

# Clean up the lunar_alt column: some rows are lists, some are floats!?
df_fcmod['lunar_alt'] = df_fcmod['lunar_alt'].apply(
    lambda x: x[0] if isinstance(x, list) else x)
df_fcmod['lunarphaseclass'] = df_fcmod['lunarphaseclass'].apply(
    lambda x: x[0] if isinstance(x, list) else x)
df_fcmod['mags'] = df_fcmod['mags'].apply(
    lambda x: x[0] if isinstance(x, list) else x)
df_fcmod['CC'] = df_fcmod['CC'].apply(
    lambda x: x[0] if isinstance(x, list) else x)

# Define the cloud cover that you want to filter out:
# coverages = ['OVC', 'SCT', 'FEW', 'BKN', 'M']
# df_fcmod = sqm_read2020.filter_sqm_cloud(df_fcmod, coverage=coverages)

# Define the lunar phases and altitudes to filter out:
# phases = ['Full', 'Gibbous', 'Crescent', 'Quarter']
# alts = [-5, -5, -5, -5]
# df_fcmod = sqm_read2020.filter_sqm_lunar(df_fcmod, lunar_phase=phases, lunar_alt=alts)

# Now let's plot!
sqm_plot2020.sqm_plot2020(df_fcmod, ars_dataframe=df_sop, plot_ars=True)
