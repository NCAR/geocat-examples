"""
NCL_overlay_1.py
===============
This script illustrates the following concepts:
   - Overlaying line contours on filled contours
   - Explicitly setting contour levels
   - Selecting a different color map for each contour plot
   
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_1.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_1_lg.png

"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/80.nc"))

# Extract slice of data
u = ds.U.isel(time=0).drop('time').isel(lev=10).drop('lev')
t = ds.T.isel(time=0).drop('time').isel(lev=10).drop('lev')

###############################################################################
# Specify levels and color map for contour
t_lev = np.arange(210, 275, 5)
cmap = gvcmaps.BlueDarkRed18

u_lev = np.arange(-5, 40, 5)

###############################################################################
# Crate plot:
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set extent around US
ax.set_extent([230, 300, 20, 60])

# Draw map features
transparent = (0, 0, 0, 0)  # RGBA value for a transparent color for lakes
ax.add_feature(cfeature.LAKES, linewidth=0.5, edgecolor='black',
               facecolor=transparent)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

# Plot filled contour
temp = t.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, levels=t_lev, extend='neither', add_colorbar=False)
plt.colorbar(temp, ax=ax, ticks=np.arange(215, 270, 5), orientation='horizontal')

# Plot line contour
u.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=u_lev, colors='black', linewidths=0.5)
plt.show()