#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NCL_polar_1_lg.py
================

This script illustrates the following concepts:
    - Drawing contours over a map using a native lat,lon grid
    - Drawing filled contours over a Lambert Conformal map
    - Zooming in on a particular area on a Lambert Conformal map
    - Subsetting a color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lcnative_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lcnative_1_lg.png
"""

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"))
# Extract a slice of the data
t = ds.pre[0,:]

###############################################################################
# Plot:

# Generate figure
plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=45, standard_parallels=(36,55))
ax = plt.axes(projection=projection, frameon=False)
ax.set_extent((30, 55, 20, 45), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)

# Plot data and create colorbar
newcmp = gvcmaps.BlueYellowRed
t.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), levels = 14, cbar_kwargs={"orientation":"horizontal",  "ticks":np.arange(0, 240, 20),  "label":'', "shrink":0.9})
plt.title(t.long_name, loc='left', size=16)
plt.title(t.units, loc='right', size=16)
plt.show()

