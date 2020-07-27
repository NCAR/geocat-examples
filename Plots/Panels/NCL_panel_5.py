"""
NCL_panel_5.py
===============
This script illustrates the following concepts:
   - Paneling three plots vertically on a page
   - Adding a common title to subplots
   - Adding a common colorbar to subplots
   - Adding figure label to subplots
   - Adding text to subplots
   - Truncating a color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_5_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays, choosing the 2nd timestamp
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)

###############################################################################
# Utility Function: Labelled Filled Contour Plot:

# Define a utility plotting function in order not to repeat many lines of codes
# since we need to make the same figure with two different variables.

def plot_labelled_filled_contours(data, ax=None, label=None):
    """
    A utility function for convenience that plots labelled, filled contours with black contours
    marking each level.It will return a dictionary containing three objects corresponding to the
    filled contours, the black contours, and the contour labels.
    """

    # Import an NCL colormap, truncating it by using geocat.viz.util convenience function
    newcmp = gvutil.truncate_colormap(gvcmaps.gui_default, minval=0.03, maxval=0.9)

    handles = dict()
    handles["filled"] = data.plot.contourf(
        ax=ax,  # this is the axes we want to plot to
        cmap=newcmp,  # our special colormap
        levels=levels,  # contour levels specified outside this function
        transform=projection,  # data projection
        add_colorbar=False,  # don't add individual colorbars for each plot call
        add_labels=False,  # turn off xarray's automatic Lat, lon labels
    )

    # matplotlib's contourf doesn't let you specify the "edgecolors" (MATLAB terminology)
    # instead we plot black contours on top of the filled contours
    handles["contour"] = data.plot.contour(
        ax=ax,
        levels=levels,
        colors="k",  # note plurals in this and following kwargs
        linestyles="-",
        linewidths=0.5,
        add_labels=False,  # again turn off automatic labels
    )

    # Label the contours
    ax.clabel(
        handles["contour"], fontsize=8, fmt="%.0f",  # Turn off decimal points
    )

    # Add coastlines and make them semitransparent for plot legibility
    ax.coastlines(linewidth=0.5, alpha=0.75)

    # Use geocat.viz.util convenience function to set axes tick values
    gvutil.set_axes_limits_and_ticks(ax, xticks=np.arange(-180, 181, 30),
                                    yticks=np.arange(-90, 91, 30))

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, labelsize=8)

    # Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)
    # Remove degree symbol from tick labels
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

    # Use geocat.viz.util convenience function to add main title as well as titles to left and right of the plot axes.
    gvutil.set_titles_and_labels(ax, lefttitle=data.attrs['long_name'], lefttitlefontsize=10,
                                 righttitle=data.attrs['units'], righttitlefontsize=10)

    # Add a label in the upper left of the axes
    ax.text(0.025, 0.9, label, transform=ax.transAxes, bbox=dict(boxstyle='square, pad=0.25', facecolor='white'))
    return handles


###############################################################################
# Plot:

# Make three panels (i.e. subplots in matplotlib) specifying white space
# between them using gridspec_kw and hspace
# Generate figure and axes using Cartopy projection
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(3, 1, figsize=(6, 10), gridspec_kw=dict(hspace=0.3),
                       subplot_kw={"projection": projection})
# Define the contour levels
levels = np.linspace(-10, 50, 13)

# Contour-plot U data, save "handles" to add a colorbar later
handles = plot_labelled_filled_contours(ds.U, ax=ax[0], label='a)')

# Set a common title
plt.suptitle("A common title", fontsize=16, y=0.94)

# Contour-plot V data
plot_labelled_filled_contours(ds.V, ax=ax[1], label='b)')

# Contour-plot U data again but in the bottom axes
plot_labelled_filled_contours(ds.U, ax=ax[2], label='c)')

# Create inset axes for colorbar
cax = inset_axes(ax[2], width='100%', height='7%', loc='lower left',
                 bbox_to_anchor=(0, -0.25, 1, 1),
                 bbox_transform=ax[2].transAxes,
                 borderpad=0)
# Add horizontal colorbar
cbar = plt.colorbar(handles["filled"], cax=cax, orientation="horizontal",
                    ticks=levels[:-1], drawedges=True, aspect=30, 
                    extendrect=True, extendfrac='auto', shrink=0.8)
cbar.ax.tick_params(labelsize=10)

# Add figure label underneath subplots
fig.text(0.5, 0.015, "Figure 1: A nifty panel plot", horizontalalignment='center', fontsize=14)

# Show the plot
plt.show()
