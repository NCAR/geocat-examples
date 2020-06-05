#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:12:34 2020

@author: misi1684
"""


import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil
import cartopy.feature as cfeature

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"))

# Extract a slice of the data
t = ds.pre[0, :]

# gvutil.xr_add_cyclic_longitudes(t,'lon')

fig = plt.figure(figsize=(12, 12))

# Generate axes, using Cartopy, drawing coastlines, and adding features
projection = ccrs.PlateCarree()
ax1 = plt.subplot(2, 2, 1, projection=projection)
ax1.coastlines(linewidths=0.5)
ax1.add_feature(cfeature.LAND, facecolor="lightgray")

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Contourf-plot data
heatmap = t.plot.contourf(
    ax=ax1,
    cmap=newcmp,
    transform=ccrs.PlateCarree(),
    levels=14,
    cbar_kwargs={
        "orientation": "horizontal",
        "ticks": np.arange(0, 240, 20),
        "label": "",
        "shrink": 0.9,
    },
)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(
    ax1,
    xlim=(30, 55),
    ylim=(20, 45),
    xticks=np.linspace(30, 55, 6),
    yticks=np.linspace(20, 45, 6),
)

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax1)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax1, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(
    ax1,
    maintitle="Rainbow Color Projection \n of Rain Fall Total",
    maintitlefontsize=16,
    righttitlefontsize=14,
    xlabel="",
    ylabel="",
)

ax2 = plt.subplot(2, 2, 2, projection=projection)
ax2.coastlines(linewidths=0.5)
ax2.add_feature(cfeature.LAND, facecolor="lightgray")

# Import an NCL colormap
newcmp = "viridis"

# Contourf-plot data
heatmap = t.plot.contourf(
    ax=ax2,
    cmap=newcmp,
    transform=ccrs.PlateCarree(),
    levels=14,
    cbar_kwargs={
        "orientation": "horizontal",
        "ticks": np.arange(0, 240, 20),
        "label": "",
        "shrink": 0.9,
    },
)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(
    ax2,
    xlim=(30, 55),
    ylim=(20, 45),
    xticks=np.linspace(30, 55, 6),
    yticks=np.linspace(20, 45, 6),
)

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax2)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax2, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(
    ax2,
    maintitle="Viridis Color Projection \n of Rain Fall Total",
    maintitlefontsize=16,
    xlabel="",
    ylabel="",
)

ax3 = plt.subplot(2, 2, 3, projection=projection)
ax3.coastlines(linewidths=0.5)
ax3.add_feature(cfeature.LAND, facecolor="lightgray")
plt.subplots_adjust(wspace=0.5)
# Import an NCL colormap
newcmp = "coolwarm"

# Contourf-plot data
heatmap = t.plot.contourf(
    ax=ax3,
    cmap=newcmp,
    transform=ccrs.PlateCarree(),
    levels=14,
    cbar_kwargs={
        "orientation": "horizontal",
        "ticks": np.arange(0, 240, 20),
        "label": "",
        "shrink": 0.9,
    },
)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(
    ax3,
    xlim=(30, 55),
    ylim=(20, 45),
    xticks=np.linspace(30, 55, 6),
    yticks=np.linspace(20, 45, 6),
)

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax3)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax3, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(
    ax3,
    maintitle="Coolwarm Diverging Color \n Projection of Rain Fall Total",
    maintitlefontsize=16,
    xlabel="",
    ylabel="",
)

ax4 = plt.subplot(2, 2, 4, projection=projection)
ax4.coastlines(linewidths=0.5)
# Change land colors from gray to green to avoid confusion
ax4.add_feature(cfeature.LAND, facecolor="lightgray")
plt.subplots_adjust(wspace=0.5)
# Import an NCL colormap
newcmp = "Blues_r"

# Contourf-plot data
heatmap = t.plot.contourf(
    ax=ax4,
    cmap=newcmp,
    transform=ccrs.PlateCarree(),
    levels=14,
    cbar_kwargs={
        "orientation": "horizontal",
        "ticks": np.arange(0, 240, 20),
        "label": "",
        "shrink": 0.9,
    },
)


# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values
gvutil.set_axes_limits_and_ticks(
    ax4,
    xlim=(30, 55),
    ylim=(20, 45),
    xticks=np.linspace(30, 55, 6),
    yticks=np.linspace(20, 45, 6),
)

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax4)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax4, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(
    ax4,
    maintitle="Blues_r Color Projection \n of Rain Fall Total",
    maintitlefontsize=16,
    xlabel="",
    ylabel="",
)

# Show the plot
plt.show()
