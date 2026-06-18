import numpy as np
import pandas as pd
import astral, sys, csv
from astral.location import Location
from astral.sun import elevation
from astral import LocationInfo
from astral import Observer
from datetime import datetime, timezone
import ephem
import zoneinfo
import meteostat
from meteostat import Point, Hourly, Stations
import warnings, requests
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_cloud_cover(lat, lon, stime, etime):
    """
    Queries the Open-Meteo API for relevant cloud-cover data;
        https://open-meteo.com/ 
    Preferably, you'll input an hour range to prevent query overloading (10,000 / day)
    Returns a DataFrame because why not...
    """

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":lat,
        'longitude':lon,
        'start_date':stime,
        'end_date':etime,
        'hourly':'cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high',
        'timezone':'UTC',
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()['hourly']
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time')
    return df

def read_sqm(fname, newfile, location, lat, lon):
    '''
    Creates a CSV based on the .txt SQM data with lunar/solar data
        - Time in UTC!
        - Split each year into a separate CSV
    
    Still to impliment:
        - Cloud cover
        - Particulate matter

    Jackson Tobin 06/04/2026
    '''
        
    # Astral location
    city = LocationInfo('Fort Collins', "Colorado", 'America/Denver', latitude=lat, longitude=lon)
    obs = Observer(lat, lon)
    time_zone = zoneinfo.ZoneInfo(city.timezone)

    # Ephem location data
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = 1524

    with open(newfile, 'w', newline='') as out, open(fname, 'r', encoding='utf-8') as f:

        # Define the CSV fields based on Jeremy White's dataset
        fieldnames = ['date','mags','sunalt_deg','lunar_alt','lunar_az',
                        'lunar_fraction','lunar_phase','lunarphaseclass']
        writer = csv.DictWriter(out, fieldnames)
        writer.writeheader()

        # initialize the datetime updaters
        dt = datetime(year=2021, month=1, day=1, hour=1, minute=0)

        for i, line in enumerate(f):
            contents = line.split()

            # Get the SQM file info
            try:
                loc = contents[0]
                date = contents[1]
                time = contents[2]
                mags = contents[3]
            except:
                return None

            if i > 1:
                # cast date and time as datetime, WITH timezone info!
                date_string = date + " " + time
                dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f") # Time already in UTC!
                observer.date = dt

                # Get the lunar data from astral
                # Astral max phase == 27.99 [days]
                phase_days = astral.moon.phase(dt)
                phase = phase_days / 27.99

                # Lunar data from ephem
                moon = ephem.Moon()
                moon.compute(observer)
                mif = moon.moon_phase
                moon_alt = float(moon.alt) * (180 / np.pi)
                moon_az = float(moon.az) * (180 / np.pi)

                # Define the lunar phase class
                phase_class = (
                    "Full" if mif > 0.95 else
                    "Gibbous" if mif > 0.5 else
                    "Quarter" if mif > 0.25 else
                    "Crescent" if mif > 0.1 else
                    "New"
                    )

                # Get the phase of day:
                try:
                    sun = astral.sun.sun(city.observer, date=dt)
                except:
                    # print('Sun data not found...')
                    sun = None
                try:
                    dt_s = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=zoneinfo.ZoneInfo("America/Denver"))
                    sun_elevation = elevation(obs, dt_s)
                except:
                    print("Solar elevation not found...")
                    sun_elevation = None

                # Compile the data into one dictionary
                data = {"date":dt,
                        "mags":mags,
                        "sunalt_deg":sun_elevation,
                        "lunar_alt":moon_alt,
                        "lunar_az":moon_az,
                        "lunar_fraction":mif,
                        "lunar_phase":phase,
                        "lunarphaseclass":phase_class,
                        }

                # Write to the CSV if there's solar data
                if (sun_elevation != None):
                    writer.writerow(data)



if __name__=="__main__":

    edit = 8
    # loc, lc = f'DSZN', 'DC'
    # lat, lon = 40.59332, -105.078 # DSZN
    # loc, lc = f"SPZN", 'ST'
    # lat, lon = 40.97506677901541, -105.06883717220823# SPZN
    # loc, lc = f"HIZN", 'HT'
    # lat, lon = 40.56603741616607, -105.08267696991831 # HILT
    loc, lc = f"FCZN", 'FC'
    lat, lon = 40.48351, -105.016 # FCZN

    # Create the SQM .csv from NPS data
    print('Creating SQM DataFrame...')
    # df = read_sqm(f'/Users/jacksontobin/Local_Documents/NightTime_Research/FoCo Night Sky Team/SQM_2021-2025/sqm_ftco/SQM_{loc}.rpt', 
    #               f'./{loc}.csv', location=loc, lat=lat, lon=lon)
    df = pd.read_csv(f'./{loc}.csv')
    print("SQM data created")

    # Get the start and end datas for weather from the dataframe
    # stime = datetime.strptime(df.loc[0, 'date'], '%Y-%m-%d %H:%M:%S')
    # etime = datetime.strptime(df.loc[len(df)-1, 'date'], '%Y-%m-%d %H:%M:%S')
    stime = df.loc[0, 'date'].split(' ')[0]
    etime = df.loc[len(df)-1, 'date'].split(' ')[0]
    print(f'    {stime} to {etime}')

    # Retrieve cloud-cover data from Open-Meteo
    print('Creating cloud-cover DataFrame...')
    # df_cc = get_cloud_cover(lat, lon, stime=stime, etime=etime)
    # df_cc.to_csv(f'./{loc}_cc.csv')
    df_cc = pd.read_csv(f'./{loc}_cc.csv')
    print("Cloud-cover data created")

    # Organize the dataframes for merging...
    print('Creating merged DataFrame...')
    df_cc.drop(labels='Unnamed: 0', axis=1)
    df = df.set_index('date')
    df_cc = df_cc.set_index('time')
    df.index = pd.to_datetime(df.index)
    df_cc.index = pd.to_datetime(df_cc.index)
    df = df.sort_index()
    df_cc = df_cc.sort_index()  

    # Merge the dataframes
    df_merged = pd.merge_asof(
        df,
        df_cc,
        left_index=True,
        right_index=True,
        direction='nearest',
        tolerance=pd.Timedelta('1h')
    )

    # Save the result to a final .csv
    print("Saving to CSV...")
    df_merged.to_csv(f'./{loc}_merged.csv')
    print("Saved!")