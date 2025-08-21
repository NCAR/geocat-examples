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
from matplotlib.ticker import MaxNLocator
import xarray as xr
import numpy as np
from pyproj import Geod
from metpy.interpolate import cross_section
import cmaps

import geocat.datafiles as gdf
from geocat.comp import interp_multidim

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
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
).rename({"lat_t": "lat", "lon_t": "lon"})


# Pull out temperature
t = ds.T[0,:,:,:]
##############################################################################
# Calculate the great circle transect

leftlat = -60
rightlat = -30

leftlon = -60
rightlon = 20

npts = 100

geodesic = Geod(ellps="sphere")
newpts = geodesic.npts(leftlat, leftlon, rightlat, rightlon, npts=npts)
_, _, gcdist = geodesic.inv(leftlat, leftlon, rightlat, rightlon)
gcdist = gcdist/1000    # convert to km

##############################################################################
# Interpolate to great circle

lat_out = [p[0] for p in newpts]
lon_out = [p[1] for p in newpts]

transect = cross_section(t, (leftlat, leftlon), (rightlat, rightlon), interp_type="nearest")
##############################################################################
# Plot

cmap = 'viridis'
cmap = cmaps.BlAqGrYeOrReVi200

fig, ax = plt.subplots(1, 1)
p = ax.contourf(transect, cmap=cmap, levels=21, x_range=[0,90])
# ax.contourf(transect.lat, transect.z_t, transect, cmap=cmap, levels=21)
# ax.set_yscale('log')
ax.invert_yaxis()
ax.set_xlim
fig.colorbar(p)
plt.xlim(0, 90)

# Just checkin something
z = transect.z_t.values
dz = [float(b - a) for a, b in zip(z[0::], z[1::])]
ddz = [float(b - a) for a, b in zip(dz[0::], dz[1::])]

zs = [z, dz, ddz]
zss = ['z_t', 'dz_t', 'ddz_t']

zfig, zax = plt.subplots(3, 1)
plt.subplots_adjust(hspace=0.75)

for axi, zi, zsi in zip(zax, zs, zss):
    axi.axes.get_yaxis().set_visible(False)
    axi.eventplot(zi)
    axi.set_xlabel(zsi)

fig.tight_layout()
