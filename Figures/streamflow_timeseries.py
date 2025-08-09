# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 09:03:25 2025

@author: atakallou
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Create hourly time series
dates = pd.date_range("2015-10-01", "2016-10-01", freq="H")

obs_path    =  os.path.join("C:\PhD\paper 2\Git\VIC\Figures", "01022500-usgs-hourly.csv")
obs         =  pd.read_csv(obs_path)
obs['date'] =  pd.to_datetime(obs['date'])
full_range  = pd.date_range(start=obs['date'].min(), end=obs['date'].max(), freq='h')
obs         = obs.set_index('date').reindex(full_range).reset_index()
obs.rename({'index': 'date'}, axis=1, inplace=True)
obs.date = pd.to_datetime(obs.date)
obs = obs.dropna(subset=['QObs(mm/h)'])
obs = obs[obs.date.isin(dates)]
dates=dates[dates.isin(obs.date)]



values = obs['QObs(mm/h)'].to_numpy()

df = pd.DataFrame({'datetime': dates, 'value': values})

# Plot
fig, ax = plt.subplots(figsize=(16, 4))

# Plot vertical lines for each 7-day window
current = dates[0]
end_date= dates[-1]
while current < end_date:
    ax.axvline(current, color='gray', linestyle='--', linewidth=1)
    current += pd.Timedelta(days=7)

# Plot time series
ax.plot(df['datetime'], df['value'], color='black', linewidth=1.5)

# Labels and axis styling
ax.set_xlabel("Date", fontsize=14, fontweight="bold")
ax.set_ylabel("Streamflow (mm/hr)", fontsize=14, fontweight="bold")
ax.set_xlim(df['datetime'].iloc[0], df['datetime'].iloc[-1])
ax.tick_params(axis='both', labelsize=14)

plt.tight_layout()
plt.show()
