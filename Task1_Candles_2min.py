from datetime import timedelta
import pandas as pd

# skip Header
title = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

# Read file and create a DataFrame
df = pd.read_csv("RELIANCE_1m (1).csv", header=None, names=title, skiprows=1)

# Convert the Unix time to date_time format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', unit='s')

# Set the index to timestamp,
# inplace = True to make changes to the initial DataFrame
df.set_index('timestamp', inplace=True)

# Create the Timedelta which is in (days/sec/micro sec/milli sec/min/hrs/weeks)
two_min = timedelta(minutes=2)

# Resample time-series data (DateOffset/Timedelta/str) with .agg({any function you pass})
new_df = df.resample(two_min, closed='right').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).reset_index()  # will Reset to timestamp index

# will clear or drop any rows or columns with NaN value
new_df = new_df.dropna()

# need to convert the date_time format of timestamp back to Unix time
new_df['timestamp'] = new_df['timestamp'].astype('int64') // 10**9

# Write the new DataFrame to an output file
new_df.to_csv('Reliance_2_min.csv', index=False)
