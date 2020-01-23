"""
vector1
=======

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

###############################################################################
# Read in data from netCDF files
sst_in = xr.open_dataset('../../data/netcdf_files/sst8292.nc')
uv_in = xr.open_dataset('../../data/netcdf_files/uvt.nc')

###############################################################################
# Extract required variables from files

# Indices of January 1988 in each file
date_sst = sst_in['date']
date_uv = uv_in['date']
ind_sst = np.where(date_sst == 198801)[0][0]
ind_uv = np.where(date_uv == 198801)[0][0]

# Read in grid information
lat_sst = sst_in['lat']
lon_sst = sst_in['lon']
lat_uv = uv_in['lat']
lon_uv = uv_in['lon']

# Read SST and U, V
sst = sst_in['SST'].isel(time=ind_sst)
u = uv_in['U'].isel(time=ind_uv, lev=0)
v = uv_in['V'].isel(time=ind_uv, lev=0)

###############################################################################
# Make the plot

# Define levels for contour map
levels = np.arange(24,29, 0.1)

# Set up figure
fig, ax = plt.subplots(figsize=(10,7))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Sea Surface Temperature\n')

# Draw vector plot
Q = plt.quiver(lon_uv, lat_uv, u, v, color='white',
               width=.0025, scale=(4.0/.045), zorder=2)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 0.85, 0.9, 4, r'4 $m/s$', labelpos='N',
                  coordinates='figure', color='black')
# Set axis limits
plt.xlim([65, 95])
plt.ylim([5, 25])

# Set major and minor ticks
ax.tick_params("both", length=8, width=1.0, which="major",
               bottom=True, top=True, left=True, right=True)
ax.tick_params("both", length=4, width=0.5, which="minor",
               bottom=True, top=True, left=True, right=True)
plt.xticks(range(70, 95, 10))
plt.yticks(range(5, 27, 5))
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%dE'))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%dN'))
ax.minorticks_on()

# Draw SST contours
cf = ax.contourf(lon_sst, lat_sst, sst, extend='min', levels=levels,
                 cmap='rainbow', zorder=0)
cax = plt.axes((0.93, 0.125, 0.02, 0.75))
fig.colorbar(cf, ax=ax, label='$^{\circ}$ C', cax=cax,
             ticks=np.arange(24, 29, 0.3))

# Turn on continent shading
feature = cartopy.feature.NaturalEarthFeature(name='coastline',
                                              category='physical',
                                              scale='110m',
                                              edgecolor='gray',
                                              facecolor='gray',
                                              zorder=1)
ax.add_feature(feature)

# Generate plot!
plt.show()
