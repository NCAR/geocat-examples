#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:17:13 2020

@author: misi1684
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

ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"),decode_coords=True)
t = ds.pre[0,:]
fig = plt.figure(figsize=(10,10))

# Generate axes using Cartopy and draw coastlines
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(linewidths=0.5)

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Contourf-plot data (for filled contours)
a = t.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels = 14, cmap = newcmp, cbar_kwargs={"orientation":"horizontal",  "ticks":np.arange(0, 240, 20),  "label":'', "shrink":0.9})

# Contour-plot data (for borderlines)
t.plot.contour(levels = 14, linewidths=0.5, cmap='k', add_labels=False)



# Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(ax, xlim=(30,55), ylim=(20,45),
                                     xticks=np.arange(-180, 180, 5), yticks=np.arange(-90, 90, 5))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, labelsize=10)

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, maintitle="Native Lambert Conformal Grid", maintitlefontsize=16,
                                  lefttitle="Precipitation", lefttitlefontsize=14,
                                  righttitle="mm", righttitlefontsize=14, xlabel="", ylabel="")

# Show the plot
plt.show()




