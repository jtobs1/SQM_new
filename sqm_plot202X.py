import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def sqm_plot202x(dataframe, title, year, vmin, vmax):
    """
    Function to plot the SQM data from 2020
    
    Input:
        dataframe: pandas DataFrame with SQM data
    """

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(12, 12))

    # Plot the SQM measurements
    ax[0].scatter(dataframe.index, dataframe['mags'], s=0.3, color='yellow', alpha=0.3)
    ax[0].set_xlim(dataframe.index.min(), dataframe.index.max())
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(13))
    ax[0].tick_params(axis='x', rotation=45)
    ax[0].set_ylabel('mags/arcsec²')    
    ax[0].grid(linestyle='--', alpha=0.5)
    ax[0].set_ylim(vmin, vmax)
    ax[0].set_xlabel('Date')
    ax[0].set_title(f'SQM Time Series {year}')


    # Plot 2: Monthly boxplot of magnitudes, grouped by lunar phase
    dataframe['month'] = dataframe.index.month
    phases = ['New', 'Crescent', 'Quarter', 'Gibbous', 'Full']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    box_data = []
    for month in range(1, 13):
        month_data = []
        for phase in phases:
            mags = dataframe[
                            (dataframe['month'] == month)
                            & (dataframe['lunarphaseclass'] == phase)
                            ]['mags'].dropna()
            month_data.append(mags)
        box_data.append(month_data)
    # box_data is length = 12
    # each element has data for each lunar phase: length = 5
    
    # Now, each month have 5 box plots, one for each lunar phase:
    positions = []
    for month in range(12):
        base_pos = month * (len(phases) + 1) + 1
        for i in range(len(phases)):
            positions.append(base_pos + i)
    flattened_data = [mags for month_data in box_data for mags in month_data]

    ax[1].boxplot(flattened_data, positions=positions, widths=0.6, patch_artist=True,
                  boxprops=dict(facecolor='lightblue', color='blue'),
                  medianprops=dict(color='red'),
                  showfliers=False, sym='')
    ax[1].set_ylabel('mags/arcsec²')
    ax[1].set_ylim(vmin, vmax)
    # set x-tick labels to be the lunar phases at each of the positions
    ax[1].set_xticks(ticks=positions, labels=[f"{phases[i%5][0]}" for i in range(len(positions))], rotation=0)
    # Get the location acronym
    # title = str(dataframe['site'].loc[dataframe['site'].notna()].iloc[0])
    ax[1].set_title(f'Monthly SQM Magnitudes by Lunar Phase {year}: {title}')
    ax[1].grid(linestyle='--', alpha=0.5)


    # Plot 3: Box plots by cloud cover – similar to Plot 2
    coverages = ['CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'M']
    box_data_cloud = []
    for month in range(1, 13):
        month_data = []
        for cover in coverages:
            mags = dataframe[(dataframe['month'] == month)
                            & (dataframe['CC'] == cover)
                            ]['mags'].dropna()
            month_data.append(mags)
        box_data_cloud.append(month_data)
    positions_cloud = []
    for month in range(12):
        base_pos = month * (len(coverages) + 1) + 1
        for i in range(len(coverages)):
            positions_cloud.append(base_pos + i)
    flattened_data_cloud = [mags for month_data in box_data_cloud for mags in month_data]
    
    ax[2].boxplot(flattened_data_cloud, positions=positions_cloud, widths=0.6, patch_artist=True,
                  boxprops=dict(facecolor='lightgreen', color='green'),
                  medianprops=dict(color='red'),
                  showfliers=False, sym='')
    ax[2].set_xticks(ticks=positions_cloud, labels=[f"{coverages[i%6]}" for i in range(len(positions_cloud))], rotation=90)
    ax[2].set_ylabel('mags/arcsec²')
    ax[2].set_ylim(vmin, vmax)
    ax[2].set_title(f'Monthly SQM Magnitudes by Cloud Cover {year}: {title}')
    ax[2].grid(linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show() 
