"""
NCL_coneff_11.py
================
This script illustrates the following concepts:
   - Filling contours with multiple shaded patterns
   - Filling contours with stippling (solid dots)
   - Changing the size of the dot fill pattern in a contour plot
   - Overlaying a stipple pattern to show area of interest
   - Changing the density of contour shaded patterns

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/coneff_11.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/coneff_11_1_lg.png
                          https://www.ncl.ucar.edu/Applications/Images/coneff_11_2_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl

import geocat.datafiles as gdf
import geocat.viz as gv

###############################################################################
# Read in data

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/atmos.nc'), decode_times=False)

# Select meridional wind at lowest pressure level
v = ds.V.isel(time=0, lev=0)

###############################################################################
# Utility function: labelled filled contour plot

# Define a utility plotting function in order not to repeat many lines of code
# since we need to make two figures with almost the same parameters


def plot_labelled_filled_contour(title, hatchsize):
    """A utility function to plot labelled contour plots with patterned fill.

    Parameters
     ----------
     title : :class:`String`:
         The main title of the plot.

     hatchsize : :class:`Float`:
         The size of the hatch marks. Used to adjust dot size.

     Returns
     -------
       :class: `None`:

     Description
     -----------
         Produce labeled and filled contour with tickmarks and tick labels.
    """

    # Generate figure (set its size (width, height) in inches)
    plt.figure(figsize=(8, 10))
    ax = plt.axes()

    # Choose hatches to fill the contours
    hatches = ['/////', '/////', '/////', '/////', None, '..', '.', '.', '.']

    # Choose colors for the hatches
    colors = [
        'coral', 'palegreen', 'royalblue', 'lemonchiffon', 'white', 'fuchsia',
        'brown', 'cyan', 'mediumblue'
    ]

    # Create a filled contour plot
    p = v.plot.contourf(ax=ax,
                        vmin=-45.0,
                        vmax=45,
                        levels=10,
                        add_colorbar=False,
                        hatches=hatches,
                        cmap='white')

    # Set the colors for the hatches
    for i, collection in enumerate(p.collections):
        collection.set_edgecolor(colors[i % len(colors)])
        collection.set_linewidth(0.)

    # Set linewidth of hatches
    plt.rcParams['hatch.linewidth'] = hatchsize

    # Plot the contour lines
    c = v.plot.contour(ax=ax,
                       vmin=-45.0,
                       vmax=45,
                       levels=10,
                       colors='k',
                       linewidths=1,
                       add_colorbar=False,
                       linestyles='solid')

    # Add horizontal colorbar
    cbar = plt.colorbar(p,
                        orientation='horizontal',
                        shrink=0.97,
                        aspect=10,
                        pad=0.09)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_ticks(np.arange(-35, 40, 10))

    # Use geocat-viz utility function to format latitude and longitude labels
    gv.add_lat_lon_ticklabels(ax)

    # Use geocat-viz utility function to format major and minor ticks
    gv.add_major_minor_ticks(ax,
                             x_minor_per_major=2,
                             y_minor_per_major=3,
                             labelsize=16)

    # Use geocat-viz utility function to set titles and labels
    gv.set_titles_and_labels(ax,
                             maintitle=title,
                             maintitlefontsize=18,
                             lefttitle="meridional wind component",
                             lefttitlefontsize=16,
                             righttitle="m/s",
                             righttitlefontsize=16)

    # Remove default x and y labels
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    # Use geocat-viz utility function to set tick marks and tick labels
    gv.set_axes_limits_and_ticks(
        ax,
        xticks=np.arange(0, 360, 60),
        yticks=np.arange(-60, 90, 30),
        xticklabels=['0', '60E', '120E', '180', '120W', '60W'],
        yticklabels=['60S', '30S', '0', '30N', '60N'])

    plt.show()


###############################################################################
# Plot

# First plot the default dot size plot
plot_labelled_filled_contour(title="Default dot size", hatchsize=1.0)

# Then plot the increased dot size version
plot_labelled_filled_contour(title="Increased dot size", hatchsize=2.5)
