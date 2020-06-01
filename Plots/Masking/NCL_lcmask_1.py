"""
NCL_lcmask_1.py
===============
This script illustrates the following concepts:
   - Drawing filled contours over a Lambert Conformal map
   - Drawing a filled contours over a masked Lambert Conformal plot
   - Zooming in on a particular area on a Lambert Conformal map
   - Using a blue-white-red color map
   - Setting contour levels using a min/max contour level and a spacing
   - Turning off the addition of a longitude cyclic point

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://ncl.ucar.edu/Applications/Scripts/lcmask_1.ncl
    - Original NCL plot: http://ncl.ucar.edu/Applications/Images/lcmask_1_1_lg.png and http://ncl.ucar.edu/Applications/Images/lcmask_1_2_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import xarray as xr
import math

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)    # Disable time decoding due to missing necessary metadata
# Extract a slice of the data
ds = ds.isel(time=0).drop("time")
ds = ds.isel(lev=0).drop("lev")
ds = ds.V

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
ds = gvutil.xr_add_cyclic_longitudes(ds, "lon")

###############################################################################
# Plot unmasked data

# Generate figure
plt.figure(figsize=(7,10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=0, standard_parallels=(45,89))
ax = plt.axes(projection=projection, frameon=False)
ax.set_extent((0, 359, 0, 90), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)

# Plot data and create colorbar
newcmp = gvcmaps.BlWhRe

wind = ds.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), add_colorbar=False, levels=24)
plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True, ticks=np.arange(-48, 48, 8), pad=0.1, aspect=12)
plt.title(ds.long_name, loc='left', size=16)
plt.title(ds.units, loc='right', size=16)
plt.show()

###############################################################################
# Read in fresh  data and mask it

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)    # Disable time decoding due to missing necessary metadata
# Extract a slice of the data
ds = ds.isel(time=0).drop("time")
ds = ds.isel(lev=0).drop("lev")
ds = ds.V

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
ds = gvutil.xr_add_cyclic_longitudes(ds, "lon")

ds = ds.where(ds.lat>20)
ds = ds.where(ds.lat<80)
east = ds.where(ds.lon>270)
west = ds.where(ds.lon<40)
ds = east.combine_first(west)

###############################################################################
# Plot masked data

# Generate figure
plt.figure(figsize=(10,10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=-25, cutoff=20, standard_parallels=(45, 89))
ax = plt.axes(projection=projection)
ax.set_global()
ax.coastlines(linewidth=0.5)


# Create a custom boundary to achive the wedge shape
#center, radius = [0.5, 0.5], 0.5
#theta1 = 210
#theta2 = 332.5
#wedge = mpatches.Wedge(center, radius, theta1, theta2, width=0.43, transform=ax.transAxes).get_path()
#ax.set_boundary(wedge, transform=ax.transAxes)

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
start = math.radians(118)
end = math.radians(240)
theta = np.linspace(start, end, 100)
center = [0.5, 0.5]
radius_1, radius_2 = 0.075, 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
inner = verts * radius_1 + center
outer = verts * radius_2 + center
outer = np.flip(outer, axis=0)
points = np.append(inner, outer, axis=0)
circle = mpath.Path(points)

ax.set_boundary(circle, transform=ax.transAxes)

# Plot data and create colorbar
newcmp = gvcmaps.BlWhRe

wind = ds.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), add_colorbar=False, levels=24)
plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True, ticks=np.arange(-48, 48, 8), pad=0.1, aspect=12)
plt.title(ds.long_name, loc='left', size=16)
plt.title(ds.units, loc='right', size=16)
plt.show()