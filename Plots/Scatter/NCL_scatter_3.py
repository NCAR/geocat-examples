"""
NCL_scatter_3.py
================
This script illustrates the following concepts:
    - Drawing a scatter plot over a map
    - Drawing markers on a map
    - Attaching markers to a map
    - Changing the marker color and size in a map plot
    - Drawing markers on a map indicating the locations of station data
   
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/scatter_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/scatter_3_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/scatter_3_2_lg.png
                         
"""

###############################################################################
# Import packages:

import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

from geocat.viz import util as gvutil
import geocat.datafiles as gdf

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays

ds = xr.open_dataset(gdf.get("netcdf_files/95031800_sao.cdf"), decode_times=False)
lat = ds.lat.isel()
lon = ds.lon.isel()

###############################################################################
# Plot

def Plots(xext, yext, xtic, ytic, xminor, yminor, size, color):
    '''
    Creates plot using user specified variables.
    
    Parameters
    ----------
    xext : 'tuple'
        Inclusive extent of projection in format (xstart, xend) with values between -180 
        and 180.
    yext : 'tuple'
        Inclusive extent of projection in format (ystart, yend) with values between -90 
        and 90.
    xtic : 'int'
        Step number of x tick label instances in format of number between each tick.
    ytic : 'int'
        Step number of y tick label instances in format of number between each tick.
    xminor : 'int'
        Exclusive number of minor ticks between each major x-axis tick mark
    yminor : 'int'
        Exclusive number of minor ticks between each major y-axis tick mark
    size : 'int'
        Size of marker being used in format of font size number.
    color : 'str'
        Matplotlib color of marker being used in format 'color'.

    '''

    # Generate figure (set its size (width, height) in inches) and axes using Cartopy projection
    plt.figure(figsize=(12, 12))
    
    # Generate axes using Cartopy 
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, x_minor_per_major=xminor, y_minor_per_major=yminor, labelsize=14)
    
    # Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)
    
    # Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
    gvutil.set_axes_limits_and_ticks(ax, xlim=xext, ylim=yext,
                                         xticks=range(-180, 180, xtic), yticks=range(-90,90,ytic))
    # Remove the degree symbol from tick labels
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    
    # Turn on continent shading
    ax.add_feature(cfeature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=0)
    ax.add_feature(cfeature.LAKES, edgecolor='white', facecolor='white', zorder=0)
    
    # Scatter-plot the location data on the map
    plt.scatter(lon, lat, s=size, c=color, marker = '+', linewidth=0.5, zorder=1)
    
    plt.title( "Locations of stations", loc="center", 
          y=1.03, size=15, fontweight="bold")
    
    plt.show()

Plots((-180,160), (-20,90), 30, 30, 3, 3, 50, 'firebrick')
Plots((-125,-65), (20,60), 10, 10, 4, 5, 50, 'b')
