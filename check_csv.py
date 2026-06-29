import pandas as pd
import numpy as np

# Read in the CSV
fdir = '/Users/jacksontobin/Local_Documents/NightTime_Research/FoCo Night Sky Team/SQM_DATA/SQM_COMPLETE'
df = pd.read_csv(f'{fdir}/DSZN_combined.csv')

print()
print(f"min date: {np.amin(df['date'])}")
print(f"max date: {np.amax(df['date'])}")
print()
print(f"number of rows: {len(df)}")

# Add cloud-cover data
def f(row):
    '''
    classifications from:
    https://www.eoas.ubc.ca/courses/atsc113/flying/met_concepts/01-met_concepts/01c-cloud_coverage/index.html
    '''
    r = row['cloudcover']
    if (r <= 10):
        val = 'CLR' # Clear
    elif (r > 10) & (r <= 30):
        val = 'FEW' # Few
    elif (r > 30) & (r <= 50):
        val = 'SCT' # Scattered
    elif (r > 50) & (r <= 90):
        val = 'BKN' # Broken
    elif (r > 90) & (r <= 100):
        val = 'OVC' # Overcast
    else:
        val = 'M' # Missing
    return val
df['CC'] = df.apply(f, axis=1)

# Save back to CSV
df.to_csv(f'{fdir}/DSZN_combined.csv', index=False)