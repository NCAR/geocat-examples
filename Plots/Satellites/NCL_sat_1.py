"""
NCL_sat_1.py
===============
This script illustrates the following concepts:
   - Using 'astype' to unpack 'short' data
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

U = ds.slp[24, :, :]

U = U.astype('float64')

U = U*0.01

wrap_U = gvutil.xr_add_cyclic_longitudes(U, "lon")

###############################################################################
# Create plot

fig = plt.figure(figsize=(8, 8))

proj=ccrs.Orthographic(central_longitude=270, central_latitude=45)
ax = plt.axes(projection=proj, frameon=True)
ax.set_global()

ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE, linewidth=.5)
ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')

p = wrap_U.plot.contour(ax=ax,
                        transform=ccrs.PlateCarree(),
                        linewidths=0.5,
                        levels=15,
                        cmap='black',
                        add_labels=False)

# Label contours
ax.clabel(p, inline=True, fontsize=10, colors='k', fmt="%.0f")

# Use gvutil function to set title and subtitles
gvutil.set_titles_and_labels(ax, maintitle=r"$\bf{SLP}$"+" "+r"$\bf{1963,}$"+" "+r"$\bf{January}$"+" "+r"$\bf{24th}$", maintitlefontsize=18, lefttitle="mean Daily Sea Level Pressure", lefttitlefontsize=12, righttitle="hPa", righttitlefontsize=12)

# Characteristics of text box
props = dict(facecolor='white', edgecolor='black', alpha=0.5)

# Place text box
ax.text(0.40, -0.1, 'CONTOUR FROM 948 TO 1064 BY 4', transform=ax.transAxes, fontsize=18, bbox=props, zorder=5)

plt.show()