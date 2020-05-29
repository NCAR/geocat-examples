"""
NCL_conwomap_5.py
=================
This script illustrates the following concepts:
   - Drawing a simple contour plot
   - Making an axis logarithmic in a contour plot
   - Changing the labels and tickmarks on a contour plot
   - Creating a main title
   - Attaching coordinate arrays to a variable

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conwomap_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conwomap_5_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.ticker import (ScalarFormatter, NullFormatter)

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
ds = ds.U
ds = ds.isel(time=0).drop('time')
ds = ds.isel(lon=0).drop('lon')

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
plt.figure(figsize=(7, 10))
ax = plt.axes()

# Format axes
plt.yscale('log')
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_minor_formatter(NullFormatter())
gvutil.set_axes_limits_and_ticks(ax, ylim=(200, 1000), yticks=[1000,700,500,300], xticks=np.arange(-60,90,30), xticklabels=['60S','30S','0','30N','60N'])
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=0, labelsize=14)

# Specify colormap and make colorbar
newcmap = gvcmaps.ncl_default
p = ds.plot.contourf(ax=ax, levels=13, vmin=-8, vmax=40, cmap=newcmap, add_colorbar=False, add_labels=False)
ds.plot.contour(ax=ax, levels=13, vmin=-8, vmax=40, colors='k', linewidths=0.5, linestyle='solid', add_colorbar=False, add_labels=False)
cbar = plt.colorbar(p, ax=ax, drawedges=True, extendrect=True, extendfrac='auto', ticks=np.arange(-8,44,4), orientation='horizontal', pad=0.075, aspect=10)
cbar.ax.tick_params(labelsize=14)
# Add titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Logarithmic axis", maintitlefontsize=16, lefttitle="Zonal Wind", lefttitlefontsize=14)

plt.show()
