"""
vector_3
========

Plot U & V vectors globally

https://www.ncl.ucar.edu/Applications/Scripts/vector_3.ncl
"""

###############################################################################
# Import necessary packages:
import xarray as xr
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs
import geocat.viz as gcv

###############################################################################
# Read in data from netCDF file.
# Note that when we extract ``u`` and ``v`` from the file,
# we only read every third latitude and longitude.
# This choice was made because ``geocat.viz`` doesn't offer an
# equivalent function to ncl's ``vcMinDistanceF`` yet.
file_in = xr.open_dataset('../../data/netcdf_files/uv300.nc')
ds = file_in.isel(time=1, lon=slice(0,-1,3), lat=slice(1,-1,3))

###############################################################################
# Make the plot

# Set up figure and axes
fig, ax = plt.subplots(figsize=(10,5.25))
ax = plt.axes(projection=ccrs.PlateCarree())
gcv.util.nclize_axis(ax)
gcv.util.add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xticks(range(-180, 181, 30))
plt.yticks(range(-90, 91, 30))

# Draw vector plot
# Notes
# 1. We plot every third vector in each direction, which is not as nice as vcMinDistanceF in NCL
# 2. There is no matplotlib equivalent to "CurlyVector"
Q = plt.quiver(ds['lon'], ds['lat'], ds['U'].data, ds['V'].data, color='black',
               zorder=1, pivot="middle", width=0.0007, headwidth=10)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 0.872, 0.8, 20, r'20', labelpos='N',
                  coordinates='figure', color='black', zorder=2)
ax.add_patch(plt.Rectangle((155, 65), 25, 25, facecolor='white', edgecolor='black', zorder=1))
ax.set_title('Zonal Wind', y=1.04, loc='left')
ax.set_title('m/s', y=1.04, loc='right')

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=0)

# Generate plot!
plt.show()
