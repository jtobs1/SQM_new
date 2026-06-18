import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

def regress_lunar_mags_average(df, title, year):
    dataframe = df.copy()
    
    # Mask low lunar zenith angles
    dataframe.loc[(dataframe['lunar_alt']) < 30,'mags'] = float('nan')
    # Mask Cloudy data
    dataframe.loc[(dataframe['CC']) != 'CLR', 'mags'] = float('nan')

    # Resample to daily averages
    daily = dataframe['mags'].resample('D').mean().to_frame()
    daily['month'] = daily.index.month

    # Plot that thang
    cmap = plt.get_cmap('jet',12)
    fig, ax = plt.subplots()
    for month in range(1,13):
        subset = daily[daily['month'] == month]
        if subset.empty:
            continue
        im=ax.scatter(subset.index, subset['mags'],
                   color=cmap(month-1),
                   s=2)
    # cbar = plt.colorbar(cmap)
    ax.grid(linestyle='--', alpha=0.4)
    ax.set_xlabel('Date')
    ax.set_ylabel('Mags/arcsec^2')
    ax.set_title(f"SQM Daily Averages at {title}")
    return None



def regress_lunar_mags(df, title, year):
    # Group by month; each color is a different month!
    dataframe = df.copy()
    dataframe['month'] = dataframe.index.month

    # Subset where lunar elevation >= 45º
    dataframe.loc[(dataframe['lunar_alt']) < 30, 'mags'] = float('nan')

    # ==============================
    # Plotting section
    # ==============================
    fig, ax = plt.subplots(figsize=(8, 6))
    dataframe.plot.scatter('lunar_fraction', 'mags',
                           c='month',
                           alpha=0.4,
                           marker='.',
                           cmap='jet',
                           ax=ax
                           )
    ax.set_ylim(14, 22)
    ax.set_ylabel("Brightness [mags/arcsec^2]")
    ax.set_xlabel('Moon Illumination Fraction')
    ax.grid(linestyle='--', alpha=0.3)
    plt.tight_layout()

    return None

def regress_cc_mags(df, title, year):
    # Group by month; each color is a different month!
    dataframe = df.copy()
    dataframe['month'] = dataframe.index.month

    # Ensure the that moon is not present
    dataframe.loc[(dataframe['lunar_alt'] > -10), 'mags'] = float('nan')

    # ==============================
    # Plotting section
    # ==============================
    fig, ax = plt.subplots(figsize=(8, 6))
    dataframe.plot.scatter('cloudcover_low', 'mags',
                           c='month',
                           alpha=0.4,
                           marker='.',
                           cmap='jet',
                           ax=ax
                           )
    ax.set_ylim(13, 22)
    ax.set_ylabel("Brightness [mags/arcsec^2]")
    ax.set_xlabel('Cloud Cover')
    ax.grid(linestyle='--', alpha=0.3)
    plt.tight_layout()

    return None

