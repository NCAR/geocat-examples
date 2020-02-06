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
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cmaps

from geocat.viz.util import add_lat_lon_ticklabels, nclize_axis, truncate_colormap

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
levels = np.arange(24,29, 0.1)

# Set up figure
fig, ax = plt.subplots(figsize=(10,7))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Sea Surface Temperature\n')
nclize_axis(ax, minor_per_major=5)
add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xlim([65,95])
plt.ylim([5,25])
plt.xticks(range(70, 95, 10))
plt.yticks(range(5, 27, 5))


# Draw vector plot
Q = plt.quiver(lon_uv, lat_uv, u, v, color='white',
               width=.0025, scale=(4.0/.045), zorder=2)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 94, 26, 4, r'4 $m/s$', labelpos='N', zorder=2,
                  coordinates='data', color='black')

# Draw SST contours
plt.cm.register_cmap('BlAqGrYeOrReVi200', truncate_colormap(cmaps.BlAqGrYeOrReVi200, minval=0.08, maxval=0.96, n=len(levels)))
cmap = plt.cm.get_cmap('BlAqGrYeOrReVi200', 50)
cf = ax.contourf(lon_sst, lat_sst, sst, extend='both', levels=levels,
                 cmap=cmap, zorder=0)
cax = plt.axes((0.93, 0.125, 0.02, 0.75))
fig.colorbar(cf, ax=ax, label='$^{\circ}$ C', cax=cax,
             ticks=np.arange(24, 29, 0.3), drawedges=True)

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=1)

# ax.add_feature(feature)
# Generate plot!
plt.show()
