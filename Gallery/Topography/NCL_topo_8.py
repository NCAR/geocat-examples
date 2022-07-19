"""
NCL_topo_8.py
=============
This script illustrates the following concepts:
   - Drawing a topographic map using 1' data
   - Drawing topographic data using GMT colormap

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/topo_8.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/topo_8_lg.png

"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cmaps

import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netcdf data file using xarray
ds = xr.open_dataset('~/Desktop/colorado_elev.nc')

# Select elevation data
ds = ds.z

###############################################################################
# Plot:

# Generate figure and set size
plt.figure(figsize=(12, 9))

# Generate axes, using Cartopy
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Select NCL colormap and truncate to remove blue from lower end
cmap = cmaps.OceanLakeLandSnow
newcmap = gv.truncate_colormap(cmap=cmap, minval=0.01, maxval=1)

# Plot the elevation data
elev = ds.plot.imshow(ax=ax,
                      transform=projection,
                      cmap=newcmap,
                      add_colorbar=False)

# Add colorbar
cbar = plt.colorbar(ax=ax,
                    mappable=elev,
                    orientation='horizontal',
                    pad=0.13,
                    shrink=0.9)
cbar.ax.tick_params(
    size=0,
    labelsize=14)  # Remove the tick marks from the colorbar, set label size
cbar.ax.xaxis.set_tick_params(pad=10, labelsize=16)
cbar.set_label("elevation (meters)", fontsize=23, labelpad=15)

# Use geocat-viz utility function to customize titles and labels
gv.set_titles_and_labels(ax,
                         xlabel="",
                         ylabel="",
                         maintitle="Rivers of Colorado",
                         maintitlefontsize=28)

# Use geocat-viz utility function to format x and y tick labels
gv.set_axes_limits_and_ticks(ax,
                             xlim=[-109.1, -102],
                             ylim=[36.9, 41.2],
                             xticks=np.arange(-109, 102),
                             yticks=np.arange(37, 42))

# Customize tick labels
ax.tick_params(length=8, labelsize=16, pad=10)

# Use geocat-viz utility function to add lat/lon formatting for tick labels
gv.add_lat_lon_ticklabels(ax)

# Show the plot
plt.show()
