"""
NCL_polar_8.py
==============
This script illustrates the following concepts:
    - Drawing filled contours and streamlines over a polar stereographic map
    - Drawing the northern hemisphere of a polar stereographic map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polar_8_lg.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polar_8_lg.png
"""
###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"))
u = ds.U[0, 1, :, :]
v = ds.V[0, 1, :, :]
t = ds.TS[0, :, :]

# Extract slices of data

###############################################################################
# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_U = gvutil.xr_add_cyclic_longitudes(u, "lon")
wrap_V = gvutil.xr_add_cyclic_longitudes(v, "lon")
wrap_T = gvutil.xr_add_cyclic_longitudes(t, "lon")

###############################################################################
# Plot:

# Generate axes, using Cartopy, drawing coastlines, and adding features
fig = plt.figure(figsize=(10, 12))
projection = ccrs.NorthPolarStereo()
ax = plt.axes(projection=projection)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Set map boundary to include latitudes between 0 and 40 and longitudes
# between -180 and 180 only
gvutil.set_map_boundary(ax, [-180, 180], [0, 40], south_pad=1)

# Set draw_labels to False so that you can manually manipulate it later
gl = ax.gridlines(ccrs.PlateCarree(),
                  draw_labels=False,
                  linestyle="--",
                  color='black')

# Manipulate latitude and longitude gridline numbers and spacing
gl.ylocator = mticker.FixedLocator(np.arange(0, 90, 15))
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))

# Manipulate longitude labels (0, 30 E, 60 E, ..., 30 W, etc.)
ticks = np.arange(0, 210, 30)
etick = ['0'] + [
    r'%dE' % tick for tick in ticks if (tick != 0) & (tick != 180)
] + ['180']
wtick = [r'%dW' % tick for tick in ticks if (tick != 0) & (tick != 180)]
labels = etick + wtick
xticks = np.arange(0, 360, 30)
yticks = np.full_like(xticks, -5)  # Latitude where the labels will be drawn

for xtick, ytick, label in zip(xticks, yticks, labels):
    if label == '180':
        ax.text(xtick,
                ytick,
                label,
                fontsize=14,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ccrs.Geodetic())
    elif label == '0':
        ax.text(xtick,
                ytick,
                label,
                fontsize=14,
                horizontalalignment='center',
                verticalalignment='bottom',
                transform=ccrs.Geodetic())
    else:
        ax.text(xtick,
                ytick,
                label,
                fontsize=14,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ccrs.Geodetic())

# Contour-plot U-data
p = wrap_U.plot.contour(ax=ax,
                        vmin=-8,
                        vmax=16,
                        transform=ccrs.PlateCarree(),
                        levels=np.arange(-12, 44, 4),
                        linewidths=0.5,
                        cmap='black',
                        add_labels=False)

# Use geocat.viz.util convenience function to add left and right titles
gvutil.set_titles_and_labels(ax,
                             lefttitle="Surface temperature",
                             righttitle="K")

# Show the plot
plt.show()
