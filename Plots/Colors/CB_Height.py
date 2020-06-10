#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CB_Height.py
================

This script illustrates multiple color schemes for color maps which will allow for those
impacted by color blindness to see visualizations. Using rainbow color schemes is also
a poor choice in color scheme for images that may be transferred to a black and white 
scale for printing. This code addresses a handful of options to use in place of rainbow 
color schemes for use in the matplotlib.pyplot library.

More information on this subject can be found here:
    - https://agilescientific.com/blog/2017/12/14/no-more-rainbows
    - `https://www.researchgate.net/publication/328361220 <https://www.researchgate.net/publication/328361220_The_Effect_of_Color_Scales_on_Climate_Scientists'_Objective_and_Subjective_Performance_in_Spatial_Data_Analysis_Tasks>`_

More color schemes can be found here:
    - https://matplotlib.org/3.1.1/tutorials/colors/colormaps.html
"""


import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)

# Extract variable
v = ds.PBLH.isel(time=0)

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
t = gvutil.xr_add_cyclic_longitudes(v, "lon")

###############################################################################
#Plot:

fig = plt.figure(figsize=(12, 12))

def comparison(color,row, col, pos, title):
    
# Generate axes, using Cartopy, drawing coastlines, and adding features
    projection = ccrs.PlateCarree()
    ax1 = plt.subplot(row, col, pos, projection=projection)
    ax1.coastlines(linewidths=0.5)
    ax1.add_feature(cfeature.LAND, facecolor="lightgray")
    
    # Import an NCL colormap
    newcmp = color #gvcmaps.BlAqGrYeOrRe
    
    # Contourf-plot data
    t.plot.contourf(
        ax=ax1,
        transform=projection,
        levels=40,
        vmin=100,
        vmax=1600,
        cmap=newcmp,
        cbar_kwargs={
            "orientation": "vertical",
            "ticks": np.arange(100, 1600, 100),
            "label": "",
            "shrink": 0.8,})
    
    # Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
    # Set axes limits, and tick values
    gvutil.set_axes_limits_and_ticks(
    ax1,
    xlim=(0, 90),
    ylim=(0, 90),
    xticks=np.linspace(-180, 180, 13),
    yticks=np.linspace(-90, 90, 7))
    
    # Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax1)
    
    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax1, labelsize=12)
    
    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax1,
        maintitle=title,
        maintitlefontsize=16,
        righttitlefontsize=14,
        xlabel="",
        ylabel="")

#Plot first color map
comparison(gvcmaps.BlAqGrYeOrRe, 2,2,1,"Rainbow Color Projection \n of PBL Height")

#plot second color map
comparison('magma', 2,2,2,"Magma Color Projection \n of PBL Height")

#plot third color map
comparison('coolwarm', 2,2,3, "Coolwarm Color Projection \n of PBL Height")

#Plot fourth color map
comparison('Reds', 2,2,4, "Reds Color Projection \n of PBL Height")


