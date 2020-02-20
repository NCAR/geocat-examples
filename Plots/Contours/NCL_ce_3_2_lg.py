"""
NCL_ce_3_2_lg.py
===============

This script illustrates the following concepts:
   - Drawing color-filled contours over a cylindrical equidistant map
   - Selecting a different color map
   - Changing the contour level spacing
   - Turning off contour lines
   - Comparing styles of map tickmarks labels
   - Changing the stride of the labelbar labels
   - Zooming in on a particular area on the map
   - Turning off the addition of a longitude cyclic point

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/ce_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/ce_3_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'), decode_times=False)
# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0).sel(lat_t = slice(-60,30), lon_t = slice(30,120))

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(7,7))

# Generate axes, using Cartopy, drawing coastlines, and adding features
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)
ax.coastlines(linewidths=0.5)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Contourf-plot data
heatmap = t.plot.contourf(ax=ax, transform=projection, levels=40, vmin=0, vmax=32, cmap=newcmp, add_colorbar=False)

# Add colorbar
cbar = plt.colorbar(heatmap, ticks = np.arange(0,32,2))
cbar.ax.set_yticklabels([str(i) for i in np.arange(0,32,2)])

# Adjust tick label size
ax.tick_params(labelsize=12)

# Usa geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
#gvutil.set_axes_limits_and_ticks(ax, xlim=(30,120), ylim=(-60,30),
#                                     xticks=np.linspace(-180, 180, 25), yticks=np.linspace(-90, 90, 13))
ax.set_xticks(np.linspace(-180, 180, 25))
ax.set_yticks(np.linspace(-90, 90, 13))
ax.set_xlim((30,120))
ax.set_ylim((-60,30))

# Usa geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

# # Usa geocat.viz.util convenience function to add minor and major tick lines
# gvutil.add_major_minor_ticks(ax, labelsize=12)

# Usa geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax, maintitle="15-degree major but no minor ticks", maintitlefontsize=16,
                                 lefttitle="Potential Temperature", lefttitlefontsize=14,
                                 righttitle="Celsius", righttitlefontsize=14, xlabel="", ylabel="")

# Show the plot
plt.show()
