"""
NCL_sat_3.py
================

This script illustrates the following concepts:
    - zooming into an orthographic projection
    - plotting filled contour data on an orthographic map
    - plotting lat/lon tick marks on an orthographic map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_3_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import numpy as np
import matplotlib.ticker as mticker

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Define a helper function for plotting lat/lon ticks on an orthographic plane

def plotOrthoTicks(coords, loc):

    if loc == 'zero':
        for lon, lat in coords:
            ax.text(lon, lat, '{0}\N{DEGREE SIGN}'.format(lon), va='bottom', ha='center',
                           transform=ccrs.PlateCarree())
    if loc == 'left':
        for lon, lat in coords:
            ax.text(lon, lat, '{0}\N{DEGREE SIGN} N '.format(lat), va='center', ha='right',
                           transform=ccrs.PlateCarree())

    if loc == 'right':
        for lon, lat in coords:
            ax.text(lon, lat, '{0}\N{DEGREE SIGN} N '.format(lat), va='center', ha='left',
                           transform=ccrs.PlateCarree())

    if loc == 'top':
        for lon, lat in coords:
            ax.text(lon, lat, '{0}\N{DEGREE SIGN} W '.format(-lon), va='bottom', ha='center', 
                           transform=ccrs.PlateCarree())

    if loc == 'bottom':
        for lon, lat in coords:
            ax.text(lon, lat, '{0}\N{DEGREE SIGN} W '.format(-lon), va='top', ha='center', 
                           transform=ccrs.PlateCarree())

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'), decode_times=False)

# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0)

###############################################################################
# Plot:

plt.figure(figsize=(8, 8))

ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-35, central_latitude=60), anchor='C')

ax.set_extent((-80,-10,30,80), crs = ccrs.PlateCarree())

ax.coastlines(resolution='110m')
ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=3)
ax.add_feature(cfeature.COASTLINE, linewidth=0.2, zorder=3)
ax.add_feature(cfeature.LAKES, edgecolor='black', linewidth=0.2, facecolor='white', zorder=4)

# Plot gridlines
gl = ax.gridlines(color='black', linewidth=0.2, zorder=2)
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 15))
gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 15))

# Contourf-plot data 
heatmap = t.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=60, vmin=0, vmax=32, cmap='magma', add_colorbar=False, zorder=1)

# Create colorbar ticks = np.arange(0,32,0.5),
cbar = plt.colorbar(heatmap, orientation='horizontal', extendrect=True, pad=0.05, shrink=.75, aspect=12)
cbar.ax.set_xticklabels([str(i) for i in np.arange(-1.5,28.5,3)])
cbar.outline.set_visible(False)

# Use gvutil function to set plot titles

main = r"$\bf{Example}$" + " " + r"$\bf{of}$" + " " + r"$\bf{Zooming}$" + " " + r"$\bf{a}$" + " " + r"$\bf{Sat}$" + " " + r"$\bf{Projection}$"
left = r"$\bf{Potential}$" + " " + r"$\bf{Temperature}$"
right = r"$\bf{Celsius}$"

title = gvutil.set_titles_and_labels(ax, maintitle=main, maintitlefontsize=16,
                                 lefttitle=left, lefttitlefontsize=14,
                                 righttitle=right, righttitlefontsize=14, xlabel="", ylabel="")

# Plot tick marks
plotOrthoTicks([(0, 81.7)], 'zero')
plotOrthoTicks([(-80, 30), (-76, 20), (-88, 40), (-107, 50)], 'left')
plotOrthoTicks([(-9, 30), (-6, 40), (1, 50), (13, 60)], 'right')
plotOrthoTicks([(-120, 60), (-60, 82.5)], 'top')
plotOrthoTicks([(-75, 16.0), (-60, 25.0), (-45, 29.0), (-30, 29.5), (-15, 26.5)], 'bottom')

plt.tight_layout()

plt.show()