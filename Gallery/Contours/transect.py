"""
NCL_trans_1.py
==============
Calculate and plot a transect

This script illustrates the following concepts:
  -

See following URLs to see the reproduced NCL plot & script:
  - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/trans_1.ncl
  - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/trans_1_1_lg.png

"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
from metpy.interpolate import cross_section
import cartopy.feature as cfeature

import geocat.datafiles as gdf

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

# Add attrs for CF compliance to work with metpy package
ds.time_bound.attrs['units'] = 'days since 0000-01-01 00:00:00'
ds.time_bound.attrs['calendar'] = 'noleap'
ds.time.attrs['calendar'] = 'noleap'

ds = xr.decode_cf(ds)

# format for metpy
ds = ds.metpy.assign_crs(
    grid_mapping_name='latitude_longitude', earth_radius=6371229.0
).rename({"lat_t": "lat", "lon_t": "lon"})


# Pull out temperature
t = ds.T[0, :, :, :]
##############################################################################
# Calculate the great circle transect

leftlat = -60
rightlat = -30

leftlon = -60
rightlon = 20

npts = 100

# geodesic = Geod(ellps="sphere")
# newpts = geodesic.npts(leftlat, leftlon, rightlat, rightlon, npts=npts)
# _, _, gcdist = geodesic.inv(leftlat, leftlon, rightlat, rightlon)
# gcdist = gcdist/1000    # convert to km

##############################################################################
# Interpolate to great circle

# caclulate with metpy's cross_section
transect = cross_section(t, (leftlat, leftlon), (rightlat, rightlon), steps=npts)

# drop lat/lons that only have nan values
# transect = transect.dropna(dim='index', how='all')

# format attributes for plotting
transect.attrs['long_name'] = transect.long_name + " Transect"

##############################################################################
# Plot transect

cmap = 'viridis'

# fig, ax = plt.subplots(1, 1)
# # p = ax.contourf(transect, cmap=cmap, levels=21)
# p = ax.contourf(transect.lat, transect.z_t, transect.values, cmap=cmap, levels=20)
# ax.set_yscale('log')
# ax.set_xlim
# fig.colorbar(p)
# plt.show()

fig, ax = plt.subplots(1, 1)
p = transect.plot.contourf(ax=ax, cmap=cmap, vmin=-2, vmax=19, levels=22)
ax.invert_yaxis()
plt.title(transect.long_name)

ax.set_xlabel('(lat, lon) along transect')
ax.set_xticks([transect.index.min(), transect.index.max()])
ax.set_xticklabels(['(-60, 60)', '(-30, 20)'])

# Show plots
plt.tight_layout()
plt.show()

##############################################################################
# Plot transect locations
projection = ccrs.PlateCarree()
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1, projection=projection)
ax.set_global()

# Draw land
ax.add_feature(cfeature.LAND, color='lightgrey')

# Add transect location line
ax.plot(
    [leftlon, rightlon],
    [leftlat, rightlat],
    transform=projection,
    color='red',
    linewidth=1,
)

# title plot
ax.set_title("Transect Location")

# add ticks to axes
ax.set_xticks(np.linspace(-180, 180, 13))
ax.set_yticks(np.linspace(-90, 90, 7))

# Show plots
plt.tight_layout()
plt.show()
