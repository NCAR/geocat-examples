"""
NCL_xy_4.py
===============
This script illustrates the following concepts:
   - Drawing a scatter plot
   - Changing the markers in an XY plot
   - Changing the marker color in an XY plot
   - Changing the marker size in an XY plot
   - Creating your own markers for an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_4.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_4_1_lg.png
                         https://www.ncl.ucar.edu/Applications/Images/xy_4_2_lg.png
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
ds = xr.open_dataset(gdf.get('netcdf_files/AtmJan360_xy_4.nc'), decode_times=False)

# Extract a slice of the data
ds = ds['T']
t = ds.isel(lev=0).drop('lev')
t = t.isel(lat=32).drop('lat')
t = t.isel(lon=29).drop('lon')

###############################################################################
# Plot with standard markers:
plt.figure(figsize=(8, 8))
ax = plt.axes()

plt.scatter(t.time, t.data, color='red')

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Scatter Plot", xlabel=t['time'].long_name, ylabel=t.long_name)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=4, labelsize=14)

gvutil.set_axes_limits_and_ticks(ax, xlim=(131155, 131190),
                                 ylim=(220.0, 232.0),
                                 xticklabels=[' ', 131160, ' ', 131170, ' ', 131180, ' ', 131190],
                                 yticklabels=np.arange(220.0, 233.0, 2.0))

plt.show()