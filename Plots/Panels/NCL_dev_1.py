"""
NCL_dev_1.py
===============
This script illustrates the following concepts:
   - Calculating deviation from zonal mean
   - Drawing zonal average plots
   - Moving the contour informational label into the plot
   - Changing the background color of the contour line labels
   - Spanning part of a color map for contour fill
   - Making the labelbar be vertical
   - Paneling two plots vertically on a page
   - Drawing color-filled contours over a cylindrical equidistant map
   - Using a blue-white-red color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/dev_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/dev_1_lg.png
"""

##############################################################################
# Import packages:
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

##############################################################################
# Plot:

# Specify projection for maps
proj = ccrs.PlateCarree()

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(6, 8))
grid = fig.add_gridspec(ncols=2, nrows=2, width_ratios=[0.85, 0.15])

# Create axis for original data plot
ax1 = fig.add_subplot(grid[0, 0], projection=ccrs.PlateCarree())
ax1.coastlines(linewidths=0.5)

# Create axis for zonal average plot
ax2 = fig.add_subplot(grid[0, 1])

# Create axis for deviation data plot
ax3 = fig.add_subplot(grid[1, 0], projection=ccrs.PlateCarree())
ax3.coastlines(linewidths=0.5)


plt.show()