"""
NCL_overlay_12.py
=================
This script illustrates the following concepts:
   - Overlaying WRF "dbz" on a topographic map
   - Using two different colormaps on one page
   - Using cnFillPalette to assign a color palette to contours
   - Using opacity to emphasize or subdue overlain features
   - Using "overlay" to overlay multiple contours
   - Drawing counties in the United States
   - Removing a plot that has been overlaid on another plot so it can be reused
   - Controlling whether the labelbar shows same opacity as contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_12.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_12_1_lg.png

"""

###############################################################################
# Import packages:
import numpy as np
from netCDF4 import Dataset
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from geocat.viz import util as gvutil
import cartopy.feature as cfeature
from wrf import (getvar, to_np, latlon_coords, get_cartopy)

import geocat.datafiles as gdf
import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data

# Open climate division datafile and add to xarray
wrfin = Dataset(gdf.get("netcdf_files/wrfout_d01_2003-07-15_00_00_00"),
                decode_times=True)

# Read variables
hgt = getvar(wrfin, "HGT")  # terrain height in m
lat = getvar(wrfin, "XLAT")  # latitude, south is negative
lon = getvar(wrfin, "XLONG")  # longitude, west is negative
znu = getvar(wrfin, "ZNU")  # eta values
dbz = getvar(wrfin, "dbz")[0, :, :]  # radar reflectivity in dBZ

###############################################################################
# Create plot

fig = plt.figure(figsize=(12, 8))

projection = get_cartopy(hgt)

# Add axes for lambert conformal map
ax = plt.axes(projection=projection)

# Add state boundaries other lake features
ax.add_feature(
    cfeature.STATES,
    edgecolor='black',
    #linestyle=(0, (5, 10)),
    zorder=4)

# Set latitude and longitude extent of map
#ax.set_extent([-119, -74, 18, 50], ccrs.Geodetic())

# Set contour levels
levels = np.array([1] + [i for i in range(201, 3002, 200)])

# Add filled contours
hgt.plot.contourf(ax=ax,
                  cmap=gvcmaps.OceanLakeLandSnow,
                  levels=levels,
                  transform=projection,
                  add_label=False,
                  add_colorbar=False)

dbz.plot.contourf(ax=ax,
                  cmap='magma',
                  levels=levels,
                  transform=projection,
                  add_label=False,
                  add_colorbar=False)

# Set shape name of map (which depicts the United States)
# shapename = 'admin_1_states_provinces_lakes'
# states_shp = shpreader.natural_earth(resolution='110m',
#                                       category='cultural',
#                                       name=shapename)

# # # Add outlines of each state within the United States
# for state in shpreader.Reader(states_shp).geometries():
#     ax.add_geometries([state],
#                       ccrs.PlateCarree(),
#                       facecolor='white',
#                       edgecolor='black',
#                       zorder=2)

# Set title and title fontsize of plot using gvutil function instead of matplotlib function call
gvutil.set_titles_and_labels(
    ax,
    maintitle="Reflectivity ({}) + at znu level = {:.3f}".format(
        dbz.attrs['units'], znu[1].data),
    maintitlefontsize=18)

gvutil.add_lat_lon_ticklabels(ax)

plt.show()
