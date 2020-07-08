"""
NCL_bar_2.py
===============
This script illustrates the following concepts:
   - Drawing bars instead of curves in an XY plot
   - Changing the aspect ratio of a bar plot
   - Drawing filled bars up or down based on a Y reference value
   - Setting the minimum/maximum value of the Y axis in a bar plot
   - Using named colors to indicate a fill color
   - Creating array of dates to use as x-axis tick labels
   - Creating a main title

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/bar_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/soi.nc"))
dsoik = ds.DSOI_KET
date = ds.date

num_months = np.shape(date)[0]

# Dates in the file are represented by year and month
start_year = int(date[0] / 100)
# Create array that represents data by months from start date
date_months = np.arange(0, num_months, 1)

###############################################################################
# Plot

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 4))
ax = plt.axes()

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=4, y_minor_per_major=5,
                             labelsize=14)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(-3, 3),
                                     yticks=np.linspace(-3, 3, 7),
                                     yticklabels=np.linspace(-3, 3, 7),
                                     xlim=(0, num_months),
                                     xticks=np.arange((1900-start_year)*12, num_months, 12*20),
                                     xticklabels=np.arange(1900, 1981, 20))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Darwin Southern Oscillation Index", ylabel='Anomalies')

plt.show()