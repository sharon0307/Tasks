import os
import pandas as pd
import numpy as np

# Set the current working directory
cwd = os.getcwd()

# Specify the filename
filename = "RELIANCE_1m (1).csv"

# Create the full file path
file_path = os.path.join(cwd, filename)

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

#set period
window = 50

# Calculate moving averages
df['SMA' + str(window)] = df['close'].rolling(window).mean()

# Generate signals
df['signal'] = np.where(df['close'] == df['SMA' + str(window)], np.nan, np.nan)
df['signal'] = np.where(df['close'] > df['SMA' + str(window)], 1.0, 0.0)
df['position'] = df['signal'].diff()

df['BE/SE'] = ''

# Update 'BE/SE' based on 'position'
df.loc[df['position'] == -1, 'BE/SE'] = 'BE'
df.loc[df['position'] == 1, 'BE/SE'] = 'SE'

res = df['SMA' + str(window)].first_valid_index()

# Update DataFrame based on the condition
if res is not None:
    df.loc[res, ['position', 'BE/SE']] = np.nan

# Find the first occurrence of 'SE' or 'BE'
first_value = df.index[(df['BE/SE'] == 'SE') | (df['BE/SE'] == 'BE')].min()

df.at[first_value, 'BE/SE'] = ''

df['signal'] = np.where(df['position'] == 1, 'Buy', np.where(df['position'] == -1, 'Sell', ''))

# Drop unnecessary columns
df = df.drop(columns=['position'])

# Save the DataFrame to a new CSV file
df.to_csv("SMA_with_Signals.csv", index=False)
