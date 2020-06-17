"""
NCL_xy_16.py
===============
This script illustrates the following concepts:
   - Drawing a legend inside an XY plot
   - Drawing an X reference line in an XY plot
   - Reversing the Y axis
   - Using log scaling and explicit labeling
   - Changing the labels in a legend
   - Creating a vertical profile plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_16.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_16_1_lg.png
                         https://www.ncl.ucar.edu/Applications/Images/xy_16_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import (ScalarFormatter, NullFormatter)
import matplotlib.ticker as tic

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
U = ds.U.isel(time=0).drop('time').isel(lon=0).drop('lon')

# Extract slices of the data at different latitudes using the index of the desired value
U20 = U.isel(lat=39).drop('lat')
U30 = U.isel(lat=42).drop('lat')
U40 = U.isel(lat=46).drop('lat')
U50 = U.isel(lat=49).drop('lat')

###############################################################################
# Plot with linear y axis:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 8))
ax = plt.axes()

# Format axes limits, ticks, and labels
gvutil.set_axes_limits_and_ticks(ax, xlim=(-20, 40), ylim=(1000, 0), xticks=np.arange(-20,60,10), yticks=np.arange(0,1200,200))
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=4, labelsize=14)
gvutil.set_titles_and_labels(ax, maintitle='Profile Plot', xlabel=U.long_name, ylabel=U['lev'].long_name)

# Add reference line x=0
ax.axvline(x=0, color='black', linewidth=0.5)

# Plot data
plt.plot(U20.data, U20.lev, color='black', linestyle='-', label='20N')
plt.plot(U30.data, U30.lev, color='black', linestyle='--', label='30N')
plt.plot(U40.data, U40.lev, color='black', linestyle=':', label='40N')
plt.plot(U50.data, U50.lev, color='black', linestyle='-.', label='50N')

# Add legend
plt.legend(loc='center right', frameon=False, fontsize=14, labelspacing=1)

plt.show()

###############################################################################
# Plot with logarithmic y axis:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 8))
ax = plt.axes()

# Format axes limits, ticks, and labels
plt.yscale('log')
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_minor_formatter(NullFormatter())
pressure_lvls = [1, 5, 10, 30, 50, 100, 200, 300, 400, 500, 700, 1000]
gvutil.set_axes_limits_and_ticks(ax, xlim=(-20, 40), ylim=(1000, 4), xticks=np.arange(-20,60,10), yticks=pressure_lvls)
gvutil.set_titles_and_labels(ax, maintitle='Profile Plot', xlabel=U.long_name)

# Note: Currently geocat-viz does not have a utility function for formating
# major and minor ticks on log axes.

ax.tick_params(labelsize=14)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
# Specify no minor ticks on log y axis
ax.yaxis.set_minor_locator(tic.LogLocator())

# length and width are in points and may need to change depending on figure size etc.
ax.tick_params("both", length=8, width=0.9, which="major", bottom=True,
               top=True, left=True, right=True)
ax.tick_params("both", length=4, width=0.4, which="minor", bottom=True,
               top=True, left=True, right=True)

# Plot data
plt.plot(U20.data, U20.lev, color='black', linestyle='-', label='20N')
plt.plot(U30.data, U30.lev, color='black', linestyle='--', label='30N')
plt.plot(U40.data, U40.lev, color='black', linestyle=':', label='40N')
plt.plot(U50.data, U50.lev, color='black', linestyle='-.', label='50N')

# Add legend
plt.legend(loc='center right', frameon=False, fontsize=14, labelspacing=1)

plt.show()
