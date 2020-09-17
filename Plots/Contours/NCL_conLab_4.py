"""
NCL_conLab_4.py
===============
This script illustrates the following concepts:
   - Drawing color-filled contours over a cylindrical equidistant map
   - Setting the background fill color for contour labels to white
   - Forcing labels to appear on every other contour line
   - Changing the contour level spacing
   - Zooming in on a particular area on a cylindrical equidistant map
   - Creating left and right titles
   - Creating a horizontal colorbar

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conLab_4.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conLab_4_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"), decode_times=False)
U = ds.isel(time=1, drop=True).U

# Reduce the dataset to something just bigger than the area we want to plot.
# This will improve how the contour lines are labeled
U = U.where(U.lon >= 0)
U = U.where(U.lon <= 71)
U = U.where(U.lat >= -33)
U = U.where(U.lat <= 33)

##############################################################################
# Plot:
plt.figure(figsize=(8, 8))

# Create axes using the Plate Carree rectangular projection
ax = plt.axes(projection=ccrs.PlateCarree())

# Draw map features
ax.add_feature(cfeature.LAKES,
               linewidth=0.5,
               edgecolor='black',
               facecolor='None')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

# Zoom in on region bounded by the prime meridian, 70N, 25S, and 25N
ax.set_extent([0, 70, -30, 30], crs=ccrs.PlateCarree())

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax,
                                 yticks=np.linspace(-20, 20, 3),
                                 xticks=np.linspace(0, 60, 3))

# Use geocat.viz.util convenience function to make plots look like NCL plots
# by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

# Remove the degree symbol from tick labels
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=3,
                             y_minor_per_major=4,
                             labelsize=14)

# Use geocat.viz.util convenience function to add titles to left and right of
# the plot axis
gvutil.set_titles_and_labels(ax, lefttitle=U.long_name, righttitle=U.units)

# Select a color map
cmap = gvcmaps.gui_default

# Draw filled contours
colors = U.plot.contourf(ax=ax,
                         cmap=cmap,
                         levels=np.arange(-16, 48, 4),
                         add_colorbar=False,
                         add_labels=False)
# Draw contour lines
lines = U.plot.contour(ax=ax,
                       colors='black',
                       levels=np.arange(-16, 48, 4),
                       linewidths=0.5,
                       linestyles='solid',
                       add_labels=False)

# Create horizontal colorbar
cbar = plt.colorbar(colors,
                    ticks=np.arange(-12, 44, 4),
                    orientation='horizontal',
                    drawedges=True,
                    aspect=12,
                    shrink=0.8,
                    pad=0.075)
cbar.ax.tick_params(labelsize=14)  # Make the labels larger

# Adding contour line labels, use `levels` to specify which levels to label
ax.clabel(lines, levels=np.arange(-8, 28, 8), fontsize=12, fmt='%d', inline=True)

# Set label backgrounds white
[
    txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
    for txt in lines.labelTexts
]

plt.show()
