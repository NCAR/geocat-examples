"""
NCL_vector_1.py
===============
Plot U & V vector over SST

This script illustrates the following concepts:
  - Overlaying vectors and filled contours on a map
  - Changing the scale of the vectors on the plot
  - Moving the vector reference annotation to the top right of the plot
  - Setting the color for vectors
  - Increasing the thickness of vectors

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/vector_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/vector_1_lg.png
"""

###############################################################################
# Import packages

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.datafiles as gdf
import cmaps
import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
sst_in = xr.open_dataset(gdf.get("netcdf_files/sst8292.nc"))
uv_in = xr.open_dataset(gdf.get("netcdf_files/uvt.nc"))

# Use date as the dimension rather than time
sst_in = sst_in.set_coords("date").swap_dims({"time": "date"}).drop('time')
uv_in = uv_in.set_coords("date").swap_dims({"time": "date"}).drop('time')

# Extract required variables
# Read SST and U, V for Jan 1988 (at 1000 mb for U, V)
# Note that we could use .isel() if we know the indices of date and lev
sst = sst_in['SST'].sel(date=198801)
u = uv_in['U'].sel(date=198801, lev=1000)
v = uv_in['V'].sel(date=198801, lev=1000)

# Read in grid information
lat_uv = u['lat']
lon_uv = u['lon']

###############################################################################
# Plot:

# Define map projection to use
proj = ccrs.PlateCarree()

# Use utility function to import NCL colormap
gv.truncate_colormap(cmaps.BlAqGrYeOrReVi200,
                     minval=0.08,
                     maxval=0.96,
                     name="BlAqGrYeOrReVi200")

# Define figure and axes
plt.figure(figsize=(8, 5))
ax = plt.axes(projection=proj)

# add land feature and zoom in on desired location
ax.add_feature(cfeature.LAND, facecolor="lightgrey", zorder=2)
ax.set_extent((66, 96, 5, 25), crs=ccrs.PlateCarree())

# Create the filled contour plot
sst_plot = sst.plot.contourf(ax=ax,
                             transform=proj,
                             levels=50,
                             vmin=24.0,
                             vmax=28.9,
                             cmap="BlAqGrYeOrReVi200",
                             add_colorbar=False)

# Remove default x and y labels from plot
plt.xlabel("")
plt.ylabel("")

# Add vectors onto the plot
Q = plt.quiver(lon_uv,
               lat_uv,
               u,
               v,
               color='white',
               pivot='middle',
               width=.0025,
               scale=75,
               zorder=2)

# Use geocat-viz utility function to format title
gv.set_titles_and_labels(ax,
                         maintitle='',
                         maintitlefontsize=18,
                         lefttitle="Sea Surface Temperature",
                         lefttitlefontsize=18,
                         righttitle="C",
                         righttitlefontsize=18,
                         xlabel=None,
                         ylabel=None,
                         labelfontsize=16)

# Format tick labels as latitude and longitudes
gv.add_lat_lon_ticklabels(ax=ax)

# Use geocat-viz utility function to customize tick marks
gv.set_axes_limits_and_ticks(ax,
                             xlim=(65, 95),
                             ylim=(5, 25),
                             xticks=range(70, 95, 10),
                             yticks=range(5, 27, 5))

# Remove degree symbol from tick labels
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# Add minor tick marks
gv.add_major_minor_ticks(ax,
                         x_minor_per_major=4,
                         y_minor_per_major=4,
                         labelsize=14)

# Add and customize colorbar
cbar_ticks = np.arange(24, 29, .3)
plt.colorbar(ax=ax,
             mappable=sst_plot,
             extendrect=True,
             shrink=0.88,
             aspect=10,
             ticks=cbar_ticks,
             drawedges=True)

# Draw the key for the quiver plot as a rectangle patch
rect = mpl.patches.Rectangle((91.7, 22.7),
                             3.1,
                             2.2,
                             facecolor='white',
                             edgecolor='k',
                             zorder=2)
ax.add_patch(rect)

ax.quiverkey(Q,
             0.95,
             0.9,
             3,
             '4',
             labelpos='N',
             color='black',
             coordinates='axes',
             fontproperties={'size': 14},
             labelsep=0.1,
             zorder=3)

# Show the plot
plt.show()
