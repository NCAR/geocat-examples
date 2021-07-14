"""
NCL_overlay_12.py
=================
This script illustrates the following concepts:
   - Overlaying WRF "dbz" on a topographic map
   - Using two different colormaps on one page
   - Using cnFillPalette to assign a color palette to contours
   - Using opacity to emphasize or subdue overlain features
   - Overlay multiple contours
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
# Debug information

# This print output resembles NCL printMinMax function
print("------------------------------------------")
print("{} ({}) : min={:.1f}    max={:.3f}".format(hgt.attrs['description'],
                                                  hgt.attrs['units'],
                                                  hgt.min().data,
                                                  hgt.max().data))
print("{} ({}) : min={:.1f}    max={:.3f}".format(dbz.attrs['description'],
                                                  dbz.attrs['units'],
                                                  dbz.min().data,
                                                  dbz.max().data))

###############################################################################
# Create plot

#
fig = plt.figure(figsize=(12, 8))

#proj = get_cartopy(hgt)
# Get Cartopy projection
projection = ccrs.PlateCarree()

# Add axes with Cartopy projection
ax = plt.axes(projection=projection)

# Set latitude and longitude extent of map
ax.set_extent([lon.min().data,
               lon.max().data,
               lat.min().data,
               lat.max().data], projection)

# Download the Natural Earth shapefile for country boundaries at 110m resolution
# shapename = 'admin_1_states_provinces'
# countries_shp = shpreader.natural_earth(resolution='10m',
#                                         category='cultural',
#                                         name=shapename)

# # Add country borders
# for state in shpreader.Reader(countries_shp).geometries():
#     ax.add_geometries([state],
#                       projection,
#                       facecolor='none',
#                       edgecolor='black',
#                       zorder=5)

# Add US states borders
ax.add_feature(cfeature.NaturalEarthFeature(category='cultural',
                                            name='admin_1_states_provinces',
                                            scale='10m',
                                            facecolor='none',
                                            edgecolor='black',
                                            linewidth=0.2),
               zorder=5)

# Set first contour levels
levels = np.array([1] + [i for i in range(201, 3002, 200)])

# Add filled contours
clb = ax.contourf(lon,
                  lat,
                  hgt.data,
                  cmap=gvcmaps.OceanLakeLandSnow,
                  levels=levels,
                  zorder=3)

fig.colorbar(clb, shrink=0.65, orientation='horizontal')

# Set second contourf levels for
levels = np.arange(-28, 41, 4)

clb2 = ax.contourf(lon, lat, dbz.data, cmap='magma', levels=levels, zorder=4)

fig.colorbar(clb2)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.set_axes_limits_and_ticks(ax,
                                 xticks=np.arange(-105, -84, 5),
                                 yticks=np.arange(18, 35, 2))

gvutil.add_lat_lon_ticklabels(ax)

gvutil.add_major_minor_ticks(ax,
                             y_minor_per_major=1,
                             x_minor_per_major=1,
                             labelsize="medium")

# Set title and title fontsize of plot using gvutil function instead of matplotlib function call
gvutil.set_titles_and_labels(
    ax,
    maintitle="Reflectivity ({}) at znu level = {:.3f}".format(
        dbz.attrs['units'], znu[1].data),
    maintitlefontsize=18)

plt.show()
