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
import cmaps

import geocat.viz as gv

###############################################################################
# Read in data:

# other option:
# import wxee
# wxee.Initialize()
# ee.Image("NOAA/NGDC/ETOPO1").wx.to_xarray()

# Open a netCDF data file using xarray default engine and load the data into xarrays
#ds = xr.open_dataset('~/Downloads/nsamerica.nc')
ds = xr.open_dataset('/Users/dquint/Downloads/ETOPO1_Ice_g_gmt4.grd')
ds = ds.z
# Select Band2
#ds = ds.Band2

###############################################################################
# Plot

# Generate figure and set size
plt.figure(figsize=(10, 8))

# Generate axes, using Cartopy
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

ax.coastlines(zorder=10)

# Set map extent [lonmin, lonmax, latmin, latmax]
#ax.set_extent([-120, -46, -5, 30])

# Pot the elevation data
elev = ds.plot(ax=ax,
               transform=projection,
               cmap=cmaps.GMT_relief,
               add_colorbar=False)

# Add colorbar
plt.colorbar(ax=ax, mappable=elev, orientation='horizontal')

# Use geocat-viz utility function to format major and minor tick marks
gv.add_major_minor_ticks(ax, labelsize=12)

# Use geocat-viz utility function to format title
gv.set_titles_and_labels(ax,
                         maintitle='ETOPO1',
                         maintitlefontsize=20,
                         xlabel="",
                         ylabel="")

# Use geocat-viz utility function to format x and y tick labels
# gv.set_axes_limits_and_ticks(ax,
#                              xlim=[-120, -46],
#                              ylim=[-5, 35],
#                              xticks=np.arange(-120, -45, 10),
#                              yticks=np.arange(-5, 38, 5))

# Use geocat-viz utility function to add lat/lon formatting for tick labels
gv.add_lat_lon_ticklabels(ax)

# Remove degree symbol from lat/lon labels
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# import ee

# ee.Initialize()

# import geemap

# Map = geemap.Map(center=[40, -100])

# dataset = ee.Image('NOAA/NGDC/ETOPO1')
# elevation = dataset.select('bedrock')
# elevationVis = {
#     'min': -7000.0,
#     'max': 3200.0,
#     'palette': ['#011de2', 'afafaf', '3603ff', 'fff477', 'b42109']
# }
# Map.setCenter(-37.62, 25.8, 2)
# Map.addLayer(elevation, elevationVis, 'Elevation')
