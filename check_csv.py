import pandas as pd
import numpy as np

# Read in the CSV
df = pd.read_csv('./HIZN_combined.csv')

print()
print(f"min date: {np.amin(df['date'])}")
print(f"max date: {np.amax(df['date'])}")
print()
print(f"number of rows: {len(df)}")