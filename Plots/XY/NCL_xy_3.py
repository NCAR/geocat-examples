"""
NCL_xy_3.py
===============
This script illustrates the following concepts:
   - Reversing the Y axis
   - Changing the line dash pattern in an XY plot
   - Creating your own line dash pattern for an XY plot
   - Changing the line color and thickness in an XY plot
   - Creating a vertical profile plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_3.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_3_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/xy_3_2_lg.png
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
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
ds = ds.U
ds = ds.isel(time=0).drop('time')
ds = ds.isel(lon=0).drop('lon')
ds = ds.isel(lat=42).drop('lat')

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 8))
ax = plt.gca()

# Plot data
plt.plot(ds.data, ds.lev)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=4)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(1000, 0), 
                                 xticks=np.arange(-10, 30, 5))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Profile Plot", xlabel=ds.long_name, ylabel=ds['lev'].long_name)

plt.show()

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 8))
ax = plt.gca()

# Plot data with custom line characterisitcs
# Use keyword `color` to change the line color
# Use keyword `linewidth` to change the line thickness
# Use keyword `dashes` to create a custom dash pattern
# Use keyword `dash_capstyle` to change the shape of the dash end
plt.plot(ds.data, ds.lev, color='red', linewidth=3, dashes=[3, 2, 1, 2, 1, 2, 1, 2], dash_capstyle='round')

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=4)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(1000, 0), 
                                 xticks=np.arange(-10, 30, 5))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Make your own dash pattern", xlabel=ds.long_name, ylabel=ds['lev'].long_name)

plt.show()
