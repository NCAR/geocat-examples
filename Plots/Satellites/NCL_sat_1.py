"""
NCL_sat_1.py
===============
This script illustrates the following concepts:
   - Using 'short2flt' to unpack 'short' data
   - Drawing line contours over a satellite map
   - Changing the view of a satellite map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
import cartopy.crs as ccrs
import cartopy.feature as cfeature

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"), decode_times=False)

U = ds.slp[1, :, :]
wrap_U = gvutil.xr_add_cyclic_longitudes(U, "lon")

###############################################################################
# Create plot

fig = plt.figure(figsize=(10, 10))

proj=ccrs.Orthographic(central_longitude=-90, central_latitude=45)
ax = plt.axes(projection=proj)
ax.set_global()

ax.add_feature(cfeature.LAND, facecolor='lightgray')


p = wrap_U.plot.contour(ax=ax,
                        transform=ccrs.PlateCarree(),
                        linewidths=0.5,
                        levels=30,
                        cmap='black',
                        add_labels=False)


plt.show()