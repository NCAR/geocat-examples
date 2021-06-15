"""
NCL_panel_14.py
===============
This script illustrates the following concepts:
   - Combining two sets of paneled plots on one page
   - Adding a common labelbar to paneled plots
   - Reversing the Y axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_14.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_14_lg.png
"""

##############################################################################
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

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"),
                     decode_times=False)
# Ensure longitudes range from 0 to 360 degrees
T = gvutil.xr_add_cyclic_longitudes(ds.T, "lon_t")

# Extract slices of data for each panel
T1 = T.isel(time=0).sel(lat_t=30, lon_t=180, method="nearest")
T2 = T.isel(time=0).sel(lat_t=-30, lon_t=180, method="nearest")
T3 = ds.T.isel(time=0, z_t=0).sel(lon_t=slice(270))
T4 = ds.T.isel(time=0, z_t=0).sel(lon_t=slice(200))

##############################################################################
# Plot:
fig = plt.figure(figsize=(10, 10))

grid = gridspec.GridSpec(nrows=2, ncols=2, hspace=0, figure=fig)

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(grid[0])  # upper left cell of grid
ax2 = fig.add_subplot(grid[1])  # upper right cell of grid
ax3 = fig.add_subplot(grid[2], projection=proj)  # lower left cell of grid
ax4 = fig.add_subplot(grid[3], projection=proj)  # lower right cell of grid

# Plot xy data at upper left and right plots
ax1.plot(T1, T.z_t, c='black', linewidth=0.5)
ax2.plot(T2, T.z_t, c='black', linewidth=0.5)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax=ax1,
                                 xlim=(0, 24),
                                 ylim=(0, 500000),
                                 xticks=np.arange(0, 28, 4),
                                 yticks=np.arange(0, 600000, 100000))
gvutil.set_axes_limits_and_ticks(ax=ax2,
                                 xlim=(0, 21),
                                 ylim=(0, 500000),
                                 xticks=np.arange(0, 24, 3),
                                 yticks=np.arange(0, 600000, 100000))

# Remove ticklabels on Y axis for panel 2
ax2.yaxis.set_ticklabels([])

# Use geocat.viz.util convenience function to add minor and major ticks
gvutil.add_major_minor_ticks(ax1,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)
gvutil.add_major_minor_ticks(ax2,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)

# Use geocat.viz.util convenience function to set titles without calling
# several matplotlib functions
gvutil.set_titles_and_labels(ax1,
                             maintitle=T.long_name,
                             maintitlefontsize=14,
                             ylabel=T.z_t.long_name,
                             labelfontsize=14)
gvutil.set_titles_and_labels(ax2, maintitle=T.long_name, maintitlefontsize=14)

# Invert Y axis
ax1.invert_yaxis()
ax1.xaxis.set_label_position('top')
ax1.xaxis.tick_top()
ax2.invert_yaxis()
ax2.xaxis.set_label_position('top')
ax2.xaxis.tick_top()

# Set ticks on all sides of the plots
ax1.tick_params(which='both', top=True, right=True)
ax2.tick_params(which='both', top=True, right=True)

# Specify which contour levels to draw
levels = np.arange(0, 30, 2)

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Panel 1: Contourf-plot data
T3.plot.contourf(ax=ax3,
                 levels=levels,
                 cmap=newcmp,
                 vmin=0,
                 vmax=28,
                 yticks=np.arange(-90, 91, 30),
                 add_colorbar=False,
                 add_labels=False)

# contour4 = ax4.contourf(U_1['lon'],
#                         U_1['lat'],
#                         U_1.data,
#                         cmap=cmap,
#                         norm=divnorm,
#                         levels=levels,
#                         extend='both')

# Show the plot
plt.show()
