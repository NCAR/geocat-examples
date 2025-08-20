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
from pyproj import Geod

import geocat.datafiles as gdf
from geocat.comp import interp_multidim

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

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

transect = interp_multidim(t, lat_out, lon_out)

##############################################################################
# Plot

fig, ax = plt.subplots(1, 1)