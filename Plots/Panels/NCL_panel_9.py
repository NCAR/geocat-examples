"""
NCL_panel_9.py
==============
This script illustrates the following concepts:
   - Paneling an XY and polar plot on the same figure
   - Using a blue-white-red color map
   - Using indexed color to set contour fill colors
   - Filling the areas of an XY curve above and below a reference line
   - Drawing a Y reference line in an XY plot
   - Turning off the map lat/lon grid lines
   - Changing the size of a PNG image
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_9.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_9_lg.png
"""

##############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
from geocat.viz import cmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
#ds = xr.open_dataset(gdf.get("netcdf_files/nao.obs.nc"),
#                     decode_times=False) 

###############################################################################
# Plot

# Format axes
fig = plt.figure(figsize=(10, 12))

# Create grid with two rows and one column
# Use `height_ratios` to adjust the relative height of the rows
grid = gridspec.GridSpec(nrows=2, 
                         ncols=1,
                         height_ratios=[0.75, 0.25],
                         figure=fig)

# Specify the projection
proj = ccrs.NorthPolarStereo()

# Add polar plot to figure
ax1 = fig.add_subplot(grid[0], projection=proj)
ax1.coastlines()
gvutil.set_map_boundary(ax1, [-180, 180], [0, 30])

# Add XY plot to figure
ax2 = fig.add_subplot(grid[1])
gvutil.set_axes_limits_and_ticks(ax=ax2,
                                 xlim=(1920, 2015),
                                 ylim=(-4.0, 3.0))
gvutil.add_major_minor_ticks(ax=ax2,
                             x_minor_per_major=4,
                             y_minor_per_major=5)