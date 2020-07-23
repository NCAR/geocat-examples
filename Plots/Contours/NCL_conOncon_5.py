"""
NCL_conOncon_5.py
=================
This script illustrates the following concepts:
   - Overlaying individual contour lines on a polar stereographic map
   - Drawing a spaghetti contour plot
   - Increasing the thickness of contour lines
   - Explicitly setting contour levels
   - Changing the color of a contour line

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conOncon_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conOncon_5_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and
# load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/HGT500_MON_1958-1997.nc"),
                     decode_times=False)

###############################################################################
# Plot:

# Generate axes, using Cartopy, drawing coastlines, and adding features
fig = plt.figure(figsize=(8, 8))
projection = ccrs.NorthPolarStereo()
ax = plt.axes(projection=projection)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Set extent to include latitudes between 0 and 40 and longitudes between
# -180 and 180 only
ax.set_extent([-180, 180, 0, 40], ccrs.PlateCarree())

# Set draw_labels to False so that you can manually manipulate it later
gl = ax.gridlines(
    ccrs.PlateCarree(),
    draw_labels=False,
    linestyle="--",
    linewidth=1,
    color='darkgray',
    zorder=2)

# Manipulate latitude and longitude gridline numbers and spacing
gl.ylocator = mticker.FixedLocator(np.arange(0, 90, 15))
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))

# Set boundary to a circle
theta = np.linspace(0, 2 * np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# Manipulate longitude labels (0, 30 E, 60 E, ..., 30 W, etc.)
ticks = np.arange(0, 210, 30)
etick = ['0'] + [r'%dE' %
                 tick for tick in ticks if (tick != 0) & (tick != 180)] + ['180']
wtick = [
    r'%dW' %
    tick for tick in ticks if (
        tick != 0) & (
            tick != 180)]
labels = etick + wtick
xticks = [-0.8, 28, 58, 89.1, 120, 151, 182.9, -36, -63, -89, -114, -140, -151]
yticks = [-3] + [-2] + [-1] + [-1] * 2 + [-1] + [-3] + [-7] + [-7] * 3 + [-7]

for xtick, ytick, label in zip(xticks, yticks, labels):
    ax.text(xtick, ytick, label, transform=ccrs.Geodetic(), fontsize=10)

# Contour-plot data

newds = ds.isel(time=0)
s = newds.HGT
slon = gvutil.xr_add_cyclic_longitudes(s, "lon")

p = slon.plot.contour(ax=ax,
                      transform=ccrs.PlateCarree(),
                      linewidths=1.5,
                      levels=[5500],
                      colors='k',
                      add_labels=False)

colorlist = ["r", "green", "blue", "yellow", "cyan", "hotpink",
             "r", "skyblue", "navy", "lightyellow", "mediumorchid", "orange",
             "slateblue", "palegreen", "magenta", "springgreen", "pink",
             "forestgreen", "violet"]

for x in range(18):

    newds = ds.isel(time=12*x+1)
    s = newds.HGT
    slon = gvutil.xr_add_cyclic_longitudes(s, "lon")

    p = slon.plot.contour(ax=ax,
                          transform=ccrs.PlateCarree(),
                          linewidths=0.5,
                          levels=[5500],
                          colors=colorlist[x],
                          add_labels=False)

# Use geocat.viz.util convenience function to add titles
gvutil.set_titles_and_labels(ax,
                             maintitle=r"$\bf{Spaghetti}$" + " " + r"$\bf{Plot}$",
                             lefttitle=slon.long_name,
                             righttitle=slon.units)

# Make tight layout
plt.tight_layout()

# Show the plot
plt.show()
