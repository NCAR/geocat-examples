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
import xarray as xr
from wrf import getvar
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from netCDF4 import Dataset
import geocat.datafiles as gdf

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data

# Open climate division datafile and add to xarray
wrfin = Dataset(gdf.get("netcdf_files/wrfout_d01_2003-07-15_00_00_00"),
                decode_times=True)

# Open climate division datafile and add to xarray
ds = xr.open_dataset(gdf.get("netcdf_files/climdiv_prcp_1899-1999.nc"),
                     decode_times=False)

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

# Set axes [left, bottom, width, height] to ensure map takes up entire figure
ax = plt.axes([.05, -.05, .9, 1], projection=projection)

# Set latitude and longitude extent to zoom in on map
ax.set_extent([lon.min().data,
               lon.max().data,
               lat.min().data,
               lat.max().data], projection)

# Add US states borders
ax.add_feature(cfeature.NaturalEarthFeature(category='cultural',
                                            name='admin_1_states_provinces',
                                            scale='10m',
                                            facecolor='none',
                                            edgecolor='black',
                                            linewidth=0.2),
               zorder=5)

# Add US county borders
reader = shpreader.Reader('countyl010g_shp_nt00964/countyl010g.shp')
counties = list(reader.geometries())
COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())
ax.add_feature(COUNTIES,
               facecolor='none',
               edgecolor='black',
               linewidth=0.2,
               zorder=5)

# Set first contour levels
levels = np.array([0, 1] + [i for i in range(201, 3202, 200)])

# Add first filled contour
contour = ax.contourf(lon,
                      lat,
                      hgt.data,
                      alpha=0.6,
                      levels=levels,
                      cmap=gvcmaps.OceanLakeLandSnow,
                      zorder=3)

# Add first color bar
clb = fig.colorbar(contour,
                   orientation='horizontal',
                   shrink=0.7,
                   pad=0.1,
                   aspect=12,
                   ticks=levels[1:-1],
                   anchor=(0.4, 0.8),
                   drawedges=True,
                   label="Terrain Height (m)")

# Manually set color bar tick length and pad
clb.ax.xaxis.set_tick_params(length=0, pad=10)

# Set second contourf levels
levels = np.arange(-28, 41, 4)

# Add second filled contour
contour2 = ax.contourf(lon,
                       lat,
                       dbz.data,
                       cmap='magma',
                       levels=levels,
                       zorder=4)

# Set colormap and its bounds for the second contour
cmap = plt.get_cmap('magma')
colorbounds = np.arange(-30, 43, 2)

# Use colormap to create a norm and mappable for colorbar to be correctly plotted
norm = mcolors.BoundaryNorm(colorbounds, cmap.N)
mappable = cm.ScalarMappable(norm=norm, cmap=cmap)

# Add second color bar
clb2 = fig.colorbar(mappable,
                    pad=0.03,
                    aspect=10,
                    shrink=0.97,
                    ticks=levels,
                    drawedges=True)

# Manually set color bar tick length and pad
clb2.ax.yaxis.set_tick_params(length=0, pad=18, labelsize=14)

# Center align colorbar tick labels
ticklabs = clb2.ax.get_yticklabels()
clb2.ax.set_yticklabels(ticklabs, ha='center')

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.set_axes_limits_and_ticks(ax,
                                 xticks=np.arange(-105, -84, 5),
                                 yticks=np.arange(18, 35, 2))

# Use gvutil function to format latitude and longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

# Use gvutil function to add major and minor ticks
gvutil.add_major_minor_ticks(ax,
                             y_minor_per_major=1,
                             x_minor_per_major=1,
                             labelsize="xx-large")

# Set padding between tick labels and axes, and turn off ticks on top and right spines
ax.tick_params(pad=14, top=False, right=False)

# Set title and title fontsize
ax.set_title("Reflectivity ({}) at znu level = {:.3f}".format(
    dbz.attrs['units'], znu[1].data),
             fontweight='bold',
             fontsize=26,
             y=1.05)

plt.show()
