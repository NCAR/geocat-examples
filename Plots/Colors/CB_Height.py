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

Figure 1. 
   - The rainbow color scheme is problematic due to the lack of a natural perceived ordering of colors,
     perceptual changes in the colors (ex: yellow and green blend together easily), and is sensitive to 
     deficiencies in vision

Figure 2. 
   -  This is an example of a less distinct contrasting color gradient. This choice in color scheme would 
      not be a good choice for printing in black and white but may ok for individuals who 
      experience blue-green colorblindness.

Figure 3. 
  - The coolwarm diverging scheme should be used when both high and low values are interesting. 
    However, be careful using this scheme if the projection will be printed to black and white.

Figure 4.
 - This plot shows how a singular color like blue can be incredibly useful for plotting this type of data.
   This color scheme will work well for color blind impacted individuals and is black and white print friendly.
"""

###############################################################################
# Import packages:

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

def Plot(color,row, col, pos, title):
    
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
            "shrink": 0.8})
    
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
Plot(gvcmaps.BlAqGrYeOrRe, 2,2,1,"Rainbow Color Projection")

#plot second color map
Plot('magma', 2,2,2,"Magma Color Projection")

#plot third color map
Plot('coolwarm', 2,2,3, "Coolwarm Color Projection")

#Plot fourth color map
Plot('Reds', 2,2,4, "Reds Color Projection")

fig.suptitle("Projections of Planetary Boundary Layer Height", x=.5, y=.93, fontsize=18)

