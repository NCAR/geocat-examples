"""
NCL_topo_1.py
===============
This script illustrates the following concepts:
   - Drawing a topographic map using 1' data
   - Drawing topographic data using the default NCL color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/topo_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/topo_1_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset('~/Downloads/nsamerica.nc')

# Select Band2
ds = ds.Band2

###############################################################################
# Plot

# Generate figure and set size
plt.figure(figsize=(10, 7))

# Generate axes, using Cartopy
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

ax.coastlines(zorder=10)

# Set map extent [lonmin, lonmax, latmin, latmax]
ax.set_extent([-120, -46, -5, 35])

# Pot the elevation data
ds.plot(ax=ax, transform=projection, cmap='terrain', add_colorbar=False)

# Use geocat-viz utility function to format major and minor tick marks
gv.add_major_minor_ticks(ax, labelsize=12)

# Use geocat-viz utility function to format title
gv.set_titles_and_labels(ax, maintitle='ETOPO1', maintitlefontsize=20)

# Use geocat-viz utility function to format x and y tick labels
gv.set_axes_limits_and_ticks(ax,
                             xticks=np.arange(-120, -45, 10),
                             yticks=np.arange(-5, 45, 10))
# Remove degree symbol from lat/lon labels
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# Use geocat-viz utility function to add lat/lon formatting for tick labels
gv.add_lat_lon_ticklabels(ax)
