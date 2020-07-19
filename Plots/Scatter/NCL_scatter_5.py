"""
NCL_scatter_5.py
================
This script illustrates the following concepts:
   - Drawing a scatter plot with markers of different colors
   - Generating dummy data using "random_normal"
   - Drawing a legend outside an XY plot
   - Changing the markers in an XY plot
   - Changing the marker color in an XY plot
   - Changing the marker size in an XY plot
   - Manually creating a legend using markers and text
   - Adding text to a plot
   - Creating a color map using named colors
   - Moving a legend closer to a plot
   - Customizing the labels in a legend
   - Changing the orientation of a legend

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/scatter_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/scatter_5_lg.png
"""

################################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from cycler import cycler

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

################################################################################
# Generate random data with an average of 10 and a stddev of 3
npts = 300
random = np.random.default_rng()
data = random.normal(loc=10, scale=3, size=npts)

################################################################################
# Specify colors and markers
colors = ['darkgoldenrod', 'darkgreen', 'coral', 'cyan', 'firebrick',
          'darkslateblue', 'limegreen', 'goldenrod']
markers = ['+', '*', 'o', 'x', 's', '^', 'v', 'D']
plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

################################################################################
# Plot
plt.figure(figsize=(8, 8))

# Divide data into 8 bins and plot
numBins = 8
indices = np.arange(0, 300)
partitions = np.linspace(0, 20, numBins + 1)
label = "{start:.1f}:{end:.1f}"
for x in range(0, numBins):
    bins = np.where(data>partitions[x], data, np.nan)
    bins = np.where(bins<partitions[x+1], bins, np.nan)
    indices = np.where(bins!=np.nan, indices, np.nan)
    plt.scatter(indices, bins, marker=markers[x], label=label.format(start=partitions[x], end=partitions[x+1]))

legend = plt.legend(bbox_to_anchor=(0, -0.1), ncol=numBins, loc='lower left', frameon=True)
for txt in legend.get_texts():
    txt.set_ha("center") # horizontal alignment of text item
    txt.set_va("center") # vertical alignment of text item
    txt.set_x(-25) # x-position
    txt.set_y(-20) # y-position
plt.show()
