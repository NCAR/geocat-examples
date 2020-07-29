
"""
NCL_polar_1_lg.py
================
This script illustrates the following concepts:
    - Drawing black-and-white contours over a polar stereographic map
    - Drawing the northern hemisphere of a polar stereographic map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polar_1_lg.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polar_1_lg.png
"""
###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
U = ds.U[1, :, :]

###############################################################################
# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_U = gvutil.xr_add_cyclic_longitudes(U, "lon")

###############################################################################
# Plot:

# Generate axes, using Cartopy, drawing coastlines, and adding features
fig = plt.figure(figsize=(10, 10))
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
    color='k')

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
etick = ['0'] + [r'%dE' % tick 
                 for tick in ticks if (tick != 0) & (tick != 180)] + ['180']
wtick = [r'%dW' % tick 
         for tick in ticks if (tick != 0) & (tick != 180)]
labels = etick + wtick
xticks = np.arange(0, 360, 30)
yticks = np.full_like(xticks, -5)  # Latitude where the labels will be drawn

for xtick, ytick, label in zip(xticks, yticks, labels):
    if label == '180':
        ax.text(xtick, ytick, label, fontsize=14, horizontalalignment='center',
                verticalalignment='top', transform=ccrs.Geodetic())
    elif label == '0':
        ax.text(xtick, ytick, label, fontsize=14, horizontalalignment='center',
                verticalalignment='bottom', transform=ccrs.Geodetic())
    else:
        ax.text(xtick, ytick, label, fontsize=14, horizontalalignment='center',
                verticalalignment='center', transform=ccrs.Geodetic())


# Contour-plot U-data
p = wrap_U.plot.contour(ax=ax,
                        vmin=-8,
                        vmax=16,
                        transform=ccrs.PlateCarree(),
                        levels=np.arange(-12, 44, 4),
                        linewidths=0.5,
                        cmap='k',
                        add_labels=False)

ax.clabel(p, np.arange(-8, 17, 8), fmt='%d', inline=1, fontsize=14)

# Use geocat.viz.util convenience function to add left and right titles
gvutil.set_titles_and_labels(ax, lefttitle="Zonal Wind", righttitle="m/s")

# Add lower text box
ax.text(1.0, -.10, "CONTOUR FROM -12 TO 40 BY 4",
        horizontalalignment='right',
        transform=ax.transAxes,
        bbox=dict(boxstyle='square, pad=0.25',
                  facecolor='white',
                  edgecolor='black'))

# Show the plot
plt.show()
