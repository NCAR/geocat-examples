"""
NCL_overlay_11a.py
==================

Concepts illustrated:

- Overlaying vectors and filled contours on a map
- Masking out particular areas in a map
- Subsetting a color map

This script shows how to overlay contours and vectors on a map,
but with the contours limited to specific areas, and the vectors
not limited.

The point of this script is to show how to mask contours against
a geographical boundary, but in a way that allows them to be drawn
up to the boundary location. This is unlike the shapefile masking
examples, where grid points are set to missing if they fall
outside a boundary, and hence you can get blocky features close
to the boundary.

With Python's matplotlib, there are 2 general approaches to
accomplishing this:

a. You can "cover" (i.e., "over lay") geographical features on
   top of other plots using the ``zorder`` parameter to most
   rendered objects.

b. You can "clip" a plot object with a geographical boundary.

This example demonstrates approach (a).

This script is based on the NCL script originally written by
Yang Zhao (CAMS) (Chinese Academy of Meteorological Sciences).
"""

###############################################################################
# Basic Imports
# -------------

import xarray as xr
import numpy as np
import geocat.viz as gcv
import cmaps

from shapely.geometry import MultiPolygon

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import PathPatch

from cartopy.feature import ShapelyFeature, OCEAN, LAKES, LAND
from cartopy.crs import PlateCarree
from cartopy.mpl.patch import geos_to_path
from cartopy.io.shapereader import Reader as ShapeReader, natural_earth
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

###############################################################################
# Read U,V,T from the data at 500hPa
# ----------------------------------
#
# Here, we read the sample dataset with Xarray and select the ``time=0`` slice
# and the ``lev=500`` hPa level.

ds = xr.open_dataset('../../data/netcdf_files/uvt.nc').sel(time=0, lev=500)

# For convenience only, extract the U,V,T and lat and lon variables
U = ds["U"]
V = ds["V"]
T = ds["T"]

lat = ds["lat"]
lon = ds["lon"]

# Define the contour levels (T) we are interested in plotting
clevs = np.arange(228, 273, 4, dtype=float)

###############################################################################
# Create a subselection of the color map
# --------------------------------------
#
# We create a new color map that is a subselection of an existing color map

cmap = gcv.util.truncate_colormap(cmaps.BkBlAqGrYeOrReViWh200,
                                  0.1, 0.6, len(clevs),
                                  "BkBlAqGrYeOrReViWh200")

###############################################################################
# Define the map projection
# -------------------------
#
# This allows Cartopy to transform ``lat`` and ``lon`` values accurately into
# points on the matplotlib plot canvas.

crs = PlateCarree()

###############################################################################
# Construct shape boundaries
# --------------------------
#
# Using Cartopy's interface to the Natural Earth Collection of shapefiles
# and geographical shape data, we construct the geographical boundaries
# that we are interested in displaying, namely the country borders of China
# and Taiwan, the borders of Chinese provinces, and all land borders *without*
# China or Taiwan.

# Download the Natural Earth shapefile for country boundaries at 10m resolution
shapefile = natural_earth(category='cultural',
                          resolution='10m',
                          name='admin_0_countries')

# Sort the geometries in the shapefile into Chinese/Taiwanese or other
country_geos = []
other_land_geos = []
for record in ShapeReader(shapefile).records():
    if record.attributes['ADMIN'] in ['China', 'Taiwan']:
        country_geos.append(record.geometry)
    else:
        other_land_geos.append(record.geometry)

# Define a Cartopy Feature for the country borders and the land mask (i.e.,
# all other land) from the shapefile geometries, so they can be easily plotted
countries = ShapelyFeature(country_geos,
                           crs=crs,
                           facecolor='none',
                           edgecolor='black',
                           lw=1.5)
land_mask = ShapelyFeature(other_land_geos,
                           crs=crs,
                           facecolor='white',
                           edgecolor='none')

# Download the Natural Earth shapefile for the states/provinces at 10m resolution
shapefile = natural_earth(category='cultural',
                          resolution='10m',
                          name='admin_1_states_provinces')

# Extract the Chinese province borders
province_geos = [record.geometry for record in ShapeReader(shapefile).records()
                 if record.attributes['admin'] == 'China']

# Define a Cartopy Feature for the province borders, so they can be easily plotted
provinces = ShapelyFeature(province_geos,
                           crs=crs,
                           facecolor='none',
                           edgecolor='black',
                           lw=0.25)

###############################################################################
# Plot
# ----

# Create the figure and the Cartopy GeoAxes object
fig = plt.figure(figsize=(12,12))
ax = plt.axes(projection=crs)

# Define the axis tick parameters and labels
gcv.util.add_lat_lon_ticklabels(ax)
ax.minorticks_on()
ax.xaxis.set_minor_locator(AutoMinorLocator(n=4))
ax.yaxis.set_minor_locator(AutoMinorLocator(n=5))
ax.tick_params("both", length=10, width=1.0, which="major", bottom=True, left=True, labelsize=20)
ax.tick_params("both", length=7, width=0.5, which="minor", bottom=True, left=True, labelsize=20)
ax.set_extent([100, 145, 15, 55], crs=crs)
ax.set_xticks([100, 120, 140])
ax.set_yticks([20, 30, 40, 50])

# Draw the temperature contour plot with the subselected colormap
# (Place the zorder of the contour plot at the lowest level)
cf = ax.contourf(lon, lat, T, levels=clevs, cmap=cmap, zorder=1)

# Draw the color bar for the contour plot
cax = plt.axes((0.14, 0.08, 0.74, 0.02))
fig.colorbar(cf, ax=ax, cax=cax, ticks=clevs, drawedges=True, orientation='horizontal')

# Add the land mask feature on top of the contour plot (higher zorder)
ax.add_feature(land_mask, zorder=2)

# Add the OCEAN and LAKES features on top of the contour plot
ax.add_feature(OCEAN.with_scale('50m'), edgecolor='black', lw=1, zorder=2)
ax.add_feature(LAKES.with_scale('50m'), edgecolor='black', lw=1, zorder=2)

# Add the country and province features (which are transparent) on top
ax.add_feature(countries, zorder=3)
ax.add_feature(provinces, zorder=3)

# Draw the wind quiver plot on top of everything else
Q = ax.quiver(lon, lat, U, V, color='black', width=.003, scale=600., headwidth=3.75, zorder=4)

# Draw the key for the quiver plot
rect = plt.Rectangle((142, 52), 3, 3, facecolor='mediumorchid', edgecolor=None, zorder=4)
ax.add_patch(rect)
ax.quiverkey(Q, 0.9675, 0.95, 30, '30', labelpos='N', color='black',
             coordinates='axes', fontproperties={'size': 14}, labelsep=0.1)

# Add a text box to indicate the pressure level
props = dict(facecolor='white', edgecolor='none', alpha=0.8)
ax.text(105, 52.7, '500hPa', transform=crs, fontsize=18, ha='center', va='center',
        color='mediumorchid', bbox=props)

# Add title text
ax.text(0, 1.01, 'Temp', transform=ax.transAxes, fontsize=20, ha='left', va='bottom', color='black')
ax.text(1, 1.01, 'Wind', transform=ax.transAxes, fontsize=20, ha='right', va='bottom', color='black')

# Generate plot!
plt.show()
