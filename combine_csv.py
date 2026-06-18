import pandas as pd
import glob

# Read all the CSVs
csv_files = glob.glob('./SQM_data/*HIZN*.csv')
for i in csv_files:
    print(i)

# Combine all the dataframes to one CSV
combined_df = pd.concat((pd.read_csv(file) for file in csv_files), ignore_index=True)
print(len(combined_df))

# Drop duplicates
unique_df = combined_df.drop_duplicates()
print(len(unique_df))

# sort based on the dates
unique_df['date'] = pd.to_datetime(unique_df['date'])
sorted_df = unique_df.sort_values(by='date', ascending=True)

# Save to a CSV
sorted_df.to_csv('./HIZN_combined.csv')

