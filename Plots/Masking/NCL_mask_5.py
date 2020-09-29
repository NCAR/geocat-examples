"""
NCL_mask_5.py
=============
This script illustrates the following concepts:
    - Using cartopy.feature options to display map information
    - Paneling two plots on a page with 'subplots' command
    - Drawing contours
    - Explicitly setting the fill colors for contours
    - Drawing contours over land only
    - Using draw order resources to mask areas in a plot
    - Adding a label bar
    - Implementing best practices when choosing a color scheme 
    
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/mask_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/mask_5_lg.png
                         
"""

# ###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.patches as mpatches

from geocat.viz import util as gvutil
import geocat.datafiles as gdf

###############################################################################
#Read in Data

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
t = ds.TS.isel(time=0)

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_t = gvutil.xr_add_cyclic_longitudes(t, "lon")

###############################################################################
#Plot:

fig = plt.figure(figsize=(10, 15))

def Plot(row, col, pos, title):
    """
    Helper function to create two similar plots where subplot position
    and title can all be customized on the same style
    map projection.

    Args:

        row (:class: 'int'):
            number of rows necessary for subplotting of visualizations
        col (:class: 'int'):
            number of columns necessary for subplotting
        pos (:class: 'int'):
            position of visualization in m x n subplot
        title (:class: 'str'):
            title of graph in format "Title"
     """

    # Generate axes, using Cartopy, drawing coastlines, and adding features
    projection = ccrs.PlateCarree()
    ax = plt.subplot(row, col, pos, projection=projection)
    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, color="green")
    ax.add_feature(cfeature.LAKES, color="plum")
    ax.add_feature(cfeature.OCEAN, color="blue")

    # Create label names and define colors for the legend
    land = mpatches.Rectangle((0, 0), 1, 1, facecolor="green")
    lakes = mpatches.Rectangle((0, 0), 1, 1, facecolor="plum")
    ocean = mpatches.Rectangle((0, 0), 1, 1, facecolor="blue")

    labels = ['Land ', 'Lakes', 'Ocean']

    plt.legend([land, lakes, ocean], labels,
               loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax,
        maintitle=title,
        maintitlefontsize=14)

# #Plot first color map
Plot(2, 1, 1, "land sea mask using 'atmos.nc'")


def Plot2(row, col, pos, title):
    """
    Helper function to create two similar plots where subplot position
    and title can all be customized on the same style
    map projection.

    Args:

        row (:class: 'int'):
            number of rows necessary for subplotting of visualizations
        col (:class: 'int'):
            number of columns necessary for subplotting
        pos (:class: 'int'):
            position of visualization in m x n subplot
        title (:class: 'str'):
            title of graph in format "Title"
     """

    ax1 = plt.subplot(row, col, pos, projection=ccrs.PlateCarree())
    ax1.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
    ax1.coastlines(linewidths=0.5)

    plt.suptitle(title, x=0.5, y=.5, fontsize=14)

    # Import an NCL colormap
    newcmp = 'magma'

    # Contourf-plot data
    contour = wrap_t.plot.contourf(ax=ax1, transform=ccrs.PlateCarree(),
                    vmin = 235, vmax = 315, levels = 18, cmap = newcmp, add_colorbar=False)

    cbar = plt.colorbar(contour, ax=ax1, orientation='horizontal', shrink=0.75,
                    pad=0.11, extendrect=True, extendfrac='auto',
                    ticks = np.arange(240,315,5))
    cbar.ax.tick_params(labelsize=10)

    ax1.add_feature(cfeature.OCEAN, zorder=10, edgecolor='k')

    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax1,
        maintitle="",
        maintitlefontsize=14,
        righttitle="degK",
        righttitlefontsize=14,
        lefttitle="temperature",
        lefttitlefontsize=14)

Plot2(2, 1, 2, "dummy TS field (ocean-masked)")