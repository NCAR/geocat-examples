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
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 8))
ax = plt.axes()

# Format axes
gvutil.set_axes_limits_and_ticks(ax, xlim=(-20, 40), ylim=(1000, 0), xticks=np.arange(-20,60,10), yticks=np.arange(0,1200,200))
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=4, labelsize=14)
gvutil.set_titles_and_labels(ax, maintitle='Profile Plot', xlabel=U.long_name, ylabel=U['lev'].long_name, labelfontsize=16)



plt.plot(U20.data, U20.lev, color='black', linestyle='-')
plt.plot(U30.data, U30.lev, color='black', linestyle='--')
plt.plot(U40.data, U40.lev, color='black', linestyle=':')
plt.plot(U50.data, U50.lev, color='black', linestyle='-.')


plt.show()