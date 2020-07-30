"""
NCL_scatter_6.py
===============
This script illustrates the following concepts:
   - Drawing a scatter plot with markers of different colors and sizes
   - Drawing outlined and filled markers on a polar map plot
   - Generating dummy data using "random_uniform"
   - Changing the marker colors on a polar map plot
   - Changing the marker sizes on a polar map plot
   - Turning off map tickmarks
   - Turning off map fill
   - Turning off map outlines

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/scatter_6.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/scatter_6_lg.png
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
# Create dummy data:

numpoints = 100
lon = np.random.randint(-180, 180, numpoints)
lat = np.random.randint(5, 90, numpoints)
dvals  = np.random.randint(0,100, numpoints)

###############################################################################

# Generate a figure
fig = plt.figure(figsize=(8, 8))

# Create an axis with a polar stereographic projection
ax = plt.axes(projection=ccrs.NorthPolarStereo())

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

colors = ("limegreen","orange","green","red","yellow","purple","blue","red","brown","crimson","skyblue")

for x in range(numpoints):
    r=lon[x]
    t=lat[x]
    plt.polar(r, t, 'ro', color=colors[x%10])

plt.show()