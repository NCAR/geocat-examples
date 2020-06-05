#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CB_Temperature.py
================

This script illustrates the following concepts:
   - Drawing filled contours over a Mercator map
   - Setting the spacing for latitude/longitude grid lines
   - Turning off the map perimeter (boundary)
   - Making the plot larger using viewport resources
   - Turning off map fill
   - Spanning part of a color map for contour fill
   - Using 'inferno' color scheme instead of 'rainbow' to follow best practices for visualizations 

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/proj_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/proj_2_lg.png
"""


import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'), decode_times=False)
#print(ds)
# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0).sel(lat_t = slice(-60,30), lon_t = slice(30,120))

fig = plt.figure(figsize=(10,10))

# Generate axes, using Cartopy, drawing coastlines, and adding features
projection = ccrs.PlateCarree()
ax1 = plt.subplot(2,2,1,projection=projection)
ax1.coastlines(linewidths=0.5)
ax1.add_feature(cfeature.LAND, facecolor='lightgray')

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Contourf-plot data
heatmap = t.plot.contourf(ax=ax1, transform=projection, levels=40, vmin=0, vmax=32, cmap=newcmp, 
                          cbar_kwargs={"orientation":"vertical",  "ticks":np.arange(0,32,2),  "label":'', "shrink":0.7})

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(ax1, xlim=(30,120), ylim=(-60,30),
                                     xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax1)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax1, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax1, maintitle="Rainbow Color Projection \n of Temperature", maintitlefontsize=16,
                             righttitlefontsize=14, xlabel="", ylabel="")

ax2 = plt.subplot(2,2,2,projection=projection)
ax2.coastlines(linewidths=0.5)
ax2.add_feature(cfeature.LAND, facecolor='lightgray')
 
# Import an NCL colormap
newcmp = 'magma'

# Contourf-plot data
heatmap = t.plot.contourf(ax=ax2, transform=projection, levels=40, vmin=0, vmax=32, cmap=newcmp, cbar_kwargs={"orientation":"vertical",  "ticks":np.arange(0,32,2),  "label":'', "shrink":0.7})

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(ax2, xlim=(30,120), ylim=(-60,30),
                                     xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax2)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax2, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax2, maintitle="Magma Color Projection \n of Temperature", maintitlefontsize=16,
                                  xlabel="", ylabel="")

ax3 = plt.subplot(2,2,3,projection=projection)
ax3.coastlines(linewidths=0.5)
ax3.add_feature(cfeature.LAND, facecolor='lightgray')
plt.subplots_adjust(wspace=.5)   
# Import an NCL colormap
newcmp = 'coolwarm'

# Contourf-plot data
heatmap = t.plot.contourf(ax=ax3, transform=projection, levels=40, vmin=0, vmax=32, cmap=newcmp, cbar_kwargs={"orientation":"vertical",  "ticks":np.arange(0,32,2),  "label":'', "shrink":0.7})

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(ax3, xlim=(30,120), ylim=(-60,30),
                                     xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax3)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax3, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax3, maintitle="Coolwarm Diverging Color \n Projection of Temperature", maintitlefontsize=16,
                                  xlabel="", ylabel="")

ax4 = plt.subplot(2,2,4, projection=projection)
ax4.coastlines(linewidths=0.5)
#Change land colors from gray to green to avoid confusion 
ax4.add_feature(cfeature.LAND, facecolor='lightgray')
plt.subplots_adjust(wspace=.5)   
# Import an NCL colormap
newcmp = 'gnuplot2'

# Contourf-plot data
heatmap = t.plot.contourf(ax=ax4, transform=projection, levels=40, vmin=0, vmax=32, cmap=newcmp, cbar_kwargs={"orientation":"vertical",  "ticks":np.arange(0,32,2),  "label":'', "shrink":0.7})


# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(ax4, xlim=(30,120), ylim=(-60,30),
                                     xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax4)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax4, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax4, maintitle="Gnuplot2 Color Projection \n of Temperature", maintitlefontsize=16,
                                  xlabel="", ylabel="")
                             
# Show the plot
plt.show()