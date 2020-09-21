"""
NCL_panel_20.py
===============
This script illustrates the following concepts:
   - Drawing four different-sized plots on the same page using gridspec

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_20.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_20_lg.png

"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))

# Extract data from second timestep
time_0 = ds.isel(time=0).drop_vars('time')
time_1 = ds.isel(time=1).drop_vars('time')

# Ensure longitudes range from 0 to 360 degrees
U_0 = gvutil.xr_add_cyclic_longitudes(time_0.U, "lon")
U_1 = gvutil.xr_add_cyclic_longitudes(time_1.U, "lon")

###############################################################################
# Plot:
fig = plt.figure(figsize=(8, 7))

grid = gridspec.GridSpec(nrows=2,
                         ncols=2,
                         height_ratios=[0.6, 0.4],
                         figure=fig)

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(grid[0])  # upper left cell of grid
ax2 = fig.add_subplot(grid[1])  # upper right cell of grid
ax3 = fig.add_subplot(grid[2], projection=proj) # lower left cell of grid
ax4 = fig.add_subplot(grid[3], projection=proj) # lower right cell of grid

# Plot xy data
ax1.plot(U_0['lat'], U_0.isel(lon=93).drop_vars('lon').data, c='black', linewidth=0.5)
ax2.plot(U_1['lat'], U_1.isel(lon=93).drop_vars('lon').data, c='black', linewidth=0.5)

# Use geocat.viz.util convenience function to set titles without calling several matplotlib functions
gvutil.set_titles_and_labels(ax1,
                             maintitle='Time=0',
                             maintitlefontsize=10,
                             ylabel=U_0.long_name,
                             labelfontsize=10)
gvutil.set_titles_and_labels(ax2,
                             maintitle='Time=1',
                             maintitlefontsize=10)

# Draw tick labels on the right side of the top right plot
ax2.yaxis.tick_right()

for ax in [ax1, ax2]:
    # Use geocat.viz.util convenience function to set axes tick values for the contour plots
    gvutil.set_axes_limits_and_ticks(ax=ax,
                                     xlim=(-90, 90),
                                     ylim=(-20, 50),
                                     xticks=np.arange(-90, 91, 30),
                                     yticks=np.arange(-20, 51, 10),
                                     xticklabels=['90S', '60S', '30S', '0', '30N', '60N', '90N'])
    
    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=5)

# Remove tick labels for top left plot
ax1.set_yticklabels([])

plt.show()
