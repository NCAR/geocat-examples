"""
NCL_topo_4.py
===============
This script illustrates the following concepts:
   - Drawing a topographic map using 1' data
   - Drawing topographic data using GMT colormap
   - Using wget to download a dataset
   - Plotting a specific region of the world

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/topo_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/topo_4_lg.png

Note:
    In the original NCL script, the ETOPO5 dataset was used. For this example,
    we use the most current version of this data, ETOPO1.
"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.viz as gv

###############################################################################
# Read in data:

ds = xr.open_dataset('~/Desktop/aus_elev.nc').z

###############################################################################
# Plot

# Generate figure and set size
plt.figure(figsize=(10, 10))

# Generate axes, using Cartopy
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Add coastlines
ax.coastlines(zorder=10)

# Plot the elevation data
elev = ds.plot.imshow(ax=ax,
                      transform=projection,
                      cmap="gist_earth",
                      add_colorbar=False)

# Set extent of the plot
ax.set_extent([110, 155, -45, -5])

ax.add_feature(cfeature.OCEAN, zorder=2)

# Add colorbar
cbar = plt.colorbar(ax=ax,
                    mappable=elev,
                    orientation='horizontal',
                    pad=0.1,
                    shrink=0.85)
cbar.ax.tick_params(
    size=0,
    labelsize=14)  # Remove the tick marks from the colorbar, set label size
cbar.ax.xaxis.set_tick_params(pad=10)

# Use geocat-viz utility function to add left and right titles
gv.set_titles_and_labels(ax,
                         lefttitle='elevation',
                         righttitle='m',
                         maintitle='ETOPO1',
                         maintitlefontsize=23)

# Remove default x and y labels
plt.xlabel("")
plt.ylabel("")

# Use geocat-viz utility function to format x and y tick labels
gv.set_axes_limits_and_ticks(ax,
                             xlim=[110, 155],
                             ylim=[-45, -6],
                             xticks=np.arange(110, 160, 10),
                             yticks=np.arange(-45, 10, 5))

# Use geocat-viz utility function to add lat/lon formatting for tick labels
gv.add_lat_lon_ticklabels(ax)

# Format tick-marks
ax.tick_params(labelsize=14, length=8, pad=10)

# Show the plot
plt.show()
