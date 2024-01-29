from datetime import timedelta
import os
import pandas as pd
 

# skip Header
title = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

# Get the current working directory
cwd = os.getcwd()

#specify the file name 
filename = "RELIANCE_1m (1).csv"

# Create the full path
file_path = os.path.join(cwd, filename) 


# Read file and create a DataFrame
df = pd.read_csv(file_path, header=None, names=title, skiprows=1)

# Convert the Unix time to date_time format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', unit='s')

# Set the index to timestamp,
# inplace = True to make changes to the initial DataFrame
df.set_index('timestamp', inplace=True)

# Create the Timedelta which is in (days/sec/micro sec/milli sec/min/hrs/weeks)
two_min = timedelta(minutes=2)

# Resample time-series data (DateOffset/Timedelta/str) with .apply({any function you pass})
new_df = df.resample(two_min, closed='right').apply({
    'open': lambda x: x.iloc[0] if len(x) > 0 else None,  # First minute's open
    'high': lambda x: max(x.iloc[0], x.iloc[-1]) if len(x) > 0 else None,  # Max of the two minutes
    'low': lambda x: min(x.iloc[0], x.iloc[-1]) if len(x) > 0 else None,   # Min of the two minutes
    'close': lambda x: x.iloc[-1] if len(x) > 0 else None,  # Second minute's close
    'volume': 'sum'
}).dropna()  

# Reset to timestamp index
new_df.reset_index(inplace=True)

# need to convert the date_time format of timestamp back to Unix time
new_df['timestamp'] = new_df['timestamp'].astype('int64') // 10**9

# Write the new DataFrame to an output file
new_df.to_csv('Updated_Reliance_2_min.csv', index=False)
