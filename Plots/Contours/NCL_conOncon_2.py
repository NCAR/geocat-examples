"""
NCL_conOncon_2.py
=================
This script illustrates the following concepts:
   - Overlaying two sets of contours on a map
   - Drawing the zero contour line thicker
   - Changing the center longitude for a cylindrical equidistant projection
   - Using a blue-white-red color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conOncon_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conOncon_2_lg.png
"""
################################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
sst = xr.open_dataset(gdf.get("netcdf_files/sst8292a.nc"))
olr = xr.open_dataset(gdf.get("netcdf_files/olr7991a.nc"))

# Extract data for December 1982
sst = sst.isel(time=11, drop=True).SSTA
olr = olr.isel(time=47, drop=True).OLRA

sst = gvutil.xr_add_cyclic_longitudes(sst, 'lon')
olr = gvutil.xr_add_cyclic_longitudes(olr, 'lon')

################################################################################
# Plot:

# Generate figure and axes
plt.figure(figsize=(8, 8))

# Set axes projection
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-160))
ax.set_extent([100, 300, -60, 60], crs=ccrs.PlateCarree())

# Draw map features on top of filled contour
ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=1)
ax.add_feature(cfeature.COASTLINE, edgecolor= 'gray', linewidth=0.5, zorder=1)

plt.show()
