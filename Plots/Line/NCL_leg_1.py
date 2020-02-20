"""
NCL_leg_1.py
===============
This script illustrates the following concepts:
   - Drawing a legend inside an XY plot
   - Changing the width and height of a legend
   - Turning off the perimeter around a legend
   - Changing the font size of legend labels
   - Customizing the labels in a legend

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/leg_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/leg_1_lg.png
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
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
# Extract slices of the data
uz = ds.U.isel(time=0).mean(dim=['lon'])
vz = ds.V.isel(time=0).mean(dim=['lon'])

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(5,5))
ax = plt.gca()

# Plot data and add a legend
plt.plot(vz.lat, vz.values, '--', dashes=[6.5, 3.7], c='gray', label='V')
plt.plot(uz.lat, uz.values, c='gray', label='U')
plt.legend(loc='upper left', frameon=False, prop={'weight':'bold'})

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=5, labelsize=12)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, tick values, and tick labels to show latitude & longitude (i.e. North (N) - South (S))
gvutil.set_axes_limits_and_ticks(ax, xlim=(-90,90), ylim=(-10,40), xticks=np.linspace(-90, 90, 7),
                                     xticklabels=['90S', '60S', '30S', '0', '30N', '60N', '90N'])

# Show the plot
plt.show()

