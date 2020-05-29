#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"))
# Extract a slice of the data
t = ds.pre[0,:]

###############################################################################
# Plot:

# Generate figure
plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=45, standard_parallels=(36,55))
ax = plt.axes(projection=projection, frameon=False)
ax.set_extent((30, 55, 20, 45), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)

# Plot data and create colorbar
newcmp = gvcmaps.BlueYellowRed
t.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), levels = 14, cbar_kwargs={"orientation":"horizontal",  "ticks":np.arange(0, 240, 20),  "label":'', "shrink":0.9})
plt.title(t.long_name, loc='left', size=16)
plt.title(t.units, loc='right', size=16)
plt.show()






# # Generate figure (set its size (width, height) in inches)
# plt.figure(figsize=(14, 7))

# # Generate axes, using Cartopy
# projection = ccrs.LambertConformal(central_longitude=45, standard_parallels=(36,55))
# ax = plt.axes(projection=projection)

# # Use global map and draw coastlines
# ax.set_global()
# ax.coastlines()

# # Import an NCL colormap
# newcmp = gvcmaps.BlueYellowRed




# # Contourf-plot data (for filled contours)
# # Note, min-max contour levels are hard-coded. contourf's automatic contour value selector produces fractional values.
# p = t.plot.contourf(ax=ax, transform=projection, vmin=-0, vmax=240, levels=20, cmap=newcmp, add_colorbar=False,
#                     extend='neither')


# # Add horizontal colorbar
# cbar = plt.colorbar(p, orientation='horizontal', shrink=0.5)
# cbar.ax.tick_params(labelsize=14)
# cbar.set_ticks(np.linspace(0, 240, 11))



# # Use geocat.viz.util convenience function to set axes tick values
# gvutil.set_axes_limits_and_ticks(ax, xlim=(30,55), ylim=(20,45),
#                                      xticks=np.arange(-180, 180, 5), yticks=np.arange(-90, 90, 5))

# # Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
# # gvutil.add_lat_lon_ticklabels(ax=ax)

# # Use geocat.viz.util convenience function to add minor and major tick lines
# gvutil.add_major_minor_ticks(ax, labelsize=12)

# # Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
# gvutil.set_titles_and_labels(ax, maintitle="Color contours mask filled land",
#                                   lefttitle=t.long_name, lefttitlefontsize=16,
#                                   righttitle=t.units, righttitlefontsize=16, xlabel="", ylabel="")



# # Show the plot
# plt.show()



