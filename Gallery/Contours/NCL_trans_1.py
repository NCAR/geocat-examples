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
from pyproj import Geod
from metpy.interpolate import cross_section

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

transect = cross_section(t, (leftlat, leftlon), (rightlat, rightlon))
##############################################################################
# Plot

fig, ax = plt.subplots(1, 1)
ax.contour(transect)