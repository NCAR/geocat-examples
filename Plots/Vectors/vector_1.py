"""
vector_1
========

Plot U & V vector over SST

https://www.ncl.ucar.edu/Applications/Scripts/vector_1.ncl
"""

###############################################################################
# Import necessary packages
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cmaps
import geocat.viz as gcv

###############################################################################
# Read in data from netCDF files
sst_in = xr.open_dataset('../../data/netcdf_files/sst8292.nc')
uv_in = xr.open_dataset('../../data/netcdf_files/uvt.nc')

# Use date as the dimension rather than time
sst_in = sst_in.set_coords("date").swap_dims({"time": "date"}).drop('time')
uv_in = uv_in.set_coords("date").swap_dims({"time": "date"}).drop('time')

###############################################################################
# Extract required variables from files

# Read SST and U, V for Jan 1988 (at 1000 mb for U, V)
# Note that we could use .isel() if we know the indices of date and lev
sst = sst_in['SST'].sel(date=198801)
u = uv_in['U'].sel(date=198801, lev=1000)
v = uv_in['V'].sel(date=198801, lev=1000)

# Read in grid information
lat_sst = sst['lat']
lon_sst = sst['lon']
lat_uv = u['lat']
lon_uv = u['lon']

###############################################################################
# Make the plot

# Define levels for contour map
# Levels are [24, 24.1, ..., 28.8, 28.9]
levels =  np.linspace(24, 28.9, 50)

# Set up figure
fig, ax = plt.subplots(figsize=(10, 7))
ax = plt.axes(projection=ccrs.PlateCarree())
gcv.util.nclize_axis(ax, minor_per_major=5)
gcv.util.add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xlim([65,95])
plt.ylim([5,25])
plt.xticks(range(70, 95, 10))
plt.yticks(range(5, 27, 5))


# Draw vector plot
Q = plt.quiver(lon_uv, lat_uv, u, v, color='white', pivot='middle',
               width=.0025, scale=75, zorder=2)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 94, 26, 4, r'4 $m/s$', labelpos='N', zorder=2,
                  coordinates='data', color='black')

# Draw SST contours
gcv.util.truncate_colormap(cmaps.BlAqGrYeOrReVi200, minval=0.08, maxval=0.96, n=len(levels), name='BlAqGrYeOrReVi200')
# cax = plt.axes((0.93, 0.125, 0.02, 0.75))
cf = sst.plot.contourf('lon', 'lat', extend='both', levels=levels,
                 cmap='BlAqGrYeOrReVi200', zorder=0, xlabel='', add_labels=False,
                 cbar_kwargs={'shrink' : 0.75, 'ticks' : np.linspace(24, 28.8, 17), 'drawedges':True, 'label' : '$^\circ$C'})
plt.title('Sea Surface Temperature\n')

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=1)

# ax.add_feature(feature)
# Generate plot!
plt.show()
