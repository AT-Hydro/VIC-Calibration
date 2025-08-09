# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 09:03:06 2025

@author: atakallou
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Generate date range
dates = pd.date_range(start="1979-01-01", end="2019-12-31", freq="D")

# Build labels
labels = []
for date in dates:
    if date <= pd.Timestamp("1980-01-10"):
        labels.append("Warm-Up")
    else:
        water_year = date.year if date.month < 10 else date.year + 1
        labels.append("Calibration" if water_year % 2 == 1 else "Validation")

# Convert labels to integers
label_types = ['Warm-Up', 'Calibration', 'Validation']
label_to_int = {label: i for i, label in enumerate(label_types)}
int_labels = np.array([[label_to_int[label] for label in labels]])

# Set colormap
colors = ['gray', 'pink', 'dodgerblue']
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(np.arange(len(label_types)+1)-0.5, cmap.N)

# --------- Main Heatmap (no colorbar) ---------
fig, ax = plt.subplots(figsize=(23, 3))
im = ax.imshow(int_labels, aspect='auto', cmap=cmap, norm=norm)

# X-axis ticks for years
year_ticks = pd.date_range(start="1979-01-01", end="2019-12-31", freq='YS')
tick_indices = [dates.get_loc(d) for d in year_ticks if d in dates]
tick_labels = [str(d.year) for d in year_ticks if d in dates]

ax.set_xticks(tick_indices)
ax.set_xticklabels(tick_labels, rotation=90, fontsize=15, fontweight='bold')
ax.set_yticks([])

plt.tight_layout()
plt.show()
fig.savefig("calibration_time.png", dpi = 300, bbox_inches='tight', pad_inches=0.01)
# --------- Separate Colorbar Figure ---------
fig_cb, ax_cb = plt.subplots(figsize=(2, 4))  # Narrow colorbar figure
cbar = plt.colorbar(
    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
    cax=ax_cb,
    ticks=range(len(label_types)),
    orientation='vertical'
)
cbar.ax.set_yticklabels(label_types, fontsize=19, fontweight='bold')
fig_cb.savefig("calibration_time_bar.png",dpi = 300, bbox_inches='tight', pad_inches=0.01)
plt.tight_layout()
plt.show()
