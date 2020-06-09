"""
NCL_overlay_6.py
===============
This script illustrates the following concepts:
   - Overlaying shaded contours on filled contours
   - Filling contours with multiple shaded patterns
   - Overlaying vectors on filled contours
   - Using the "palette" resources to assign a color palette to color vectors and contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_6.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_6_lg.png
"""

###############################################################################
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
uf = xr.open_dataset(gdf.get("netcdf_files/Ustorm.cdf"))
vf = xr.open_dataset(gdf.get("netcdf_files/Vstorm.cdf"))
pf = xr.open_dataset(gdf.get("netcdf_files/Pstorm.cdf"))
tf = xr.open_dataset(gdf.get("netcdf_files/Tstorm.cdf"))
u500f = xr.open_dataset(gdf.get("netcdf_files/U500storm.cdf"))
v500f = xr.open_dataset(gdf.get("netcdf_files/V500storm.cdf"))

p = pf.p.isel(timestep=0).drop('timestep')
t = tf.t
u = uf.u.isel(timestep=0).drop('timestep')
v = vf.v.isel(timestep=0).drop('timestep')
u500 = u500f.u.isel(timestep=0).drop('timestep')
v500 = v500f.v.isel(timestep=0).drop('timestep')
time = vf.timestep

# Convert Pa to hPa
p = p/100
# Convert K to F
t = (t - 273.15) * 9/5 + 32

###############################################################################
# Create map:
plt.figure(figsize=(10,6))
proj = ccrs.LambertAzimuthalEqualArea(central_longitude=-100, central_latitude=40)

# Set axis projection
ax = plt.axes(projection=proj)
# Set extent to include roughly the United States
transparent = (0, 0, 0, 0) # RGBA value for a transparent color
ax.set_extent((-128, -58, 18, 65), crs=ccrs.PlateCarree())
ax.add_feature(cfeature.OCEAN, color='lightskyblue', zorder=0)
ax.add_feature(cfeature.LAND, color='silver', zorder=1)
ax.add_feature(cfeature.LAKES, linewidth=0.5, edgecolor='black', facecolor=transparent, zorder=3)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)

# Import color mab for pressure level contour
p_cmap = gvcmaps.StepSeq25
pressure = p.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=p_cmap, levels=np.arange(975, 1050, 5), add_colorbar=False, add_labels=False, zorder=2)
cbar = plt.colorbar(pressure, ticks=np.arange(980, 1045, 5), label = 'Sea Level Pressure')

# Add streamline overlay
plt.streamplot(u500.lon, u500.lat, u500.data, v500.data, transform=ccrs.PlateCarree(), color='black', arrowstyle='->', linewidth=0.5, density=2, zorder=4)

# Add vector grid
# First thin the data the the vector grid is less cluttered
x = u['lon'].data[0:36:2]
y = u['lat'].data[0:33:2]
u = u.data[0:33:2,0:36:2]
v = v.data[0:33:2,0:36:2]

# Import color map for vectors
#vect_cmap = gvcmaps.amwg_blueyellowred
Q = plt.quiver(x, y, u, v, transform=ccrs.PlateCarree(), zorder=5)
plt.quiverkey(Q, 0.95, 0.05, 20, label="20")
plt.show()
