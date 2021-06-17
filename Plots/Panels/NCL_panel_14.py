"""
NCL_panel_14.py
===============
This script illustrates the following concepts:
   - Combining two sets of paneled plots on one page
   - Adding a common labelbar to paneled plots
   - Reversing the Y axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_14.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_14_lg.png
"""

##############################################################################
# Import packages:

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"),
                     decode_times=False)
# Ensure longitudes range from 0 to 360 degrees
T = gvutil.xr_add_cyclic_longitudes(ds.T, "lon_t")

# Extract slices of data for each panel
T1 = T.isel(time=0).sel(lat_t=30, lon_t=180, method="nearest")
T2 = T.isel(time=0).sel(lat_t=-30, lon_t=180, method="nearest")
T3 = T.isel(time=0).sel(lon_t=270, method="nearest")
T4 = T.isel(time=0).sel(lon_t=200, method="nearest")

##############################################################################
# Plot:
fig = plt.figure(figsize=(10, 13))

# Add the subplots
ax1 = plt.subplot(2, 2, 1)  # upper left cell of grid
ax2 = plt.subplot(2, 2, 2)  # upper right cell of grid
ax3 = plt.subplot(2, 2, 3)  # lower left cell of grid
ax4 = plt.subplot(2, 2, 4)  # lower right cell of grid

# Make sure subplots are square
for axes in [ax1, ax2, ax3, ax4]:
    axes.set_box_aspect(1)

# Plot xy data at upper left and right plots
ax1.plot(T1, T.z_t, c='black', linewidth=0.5)
ax2.plot(T2, T.z_t, c='black', linewidth=0.5)

# # Display X axis ticklabels at the top
ax1.xaxis.tick_top()
ax2.xaxis.tick_top()

# Use geocat.viz.util convenience function to add minor and major ticks
gvutil.add_major_minor_ticks(ax1,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)
gvutil.add_major_minor_ticks(ax2,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax=ax1,
                                 xlim=(0, 24),
                                 ylim=(500000, 0),
                                 xticks=np.arange(0, 28, 4),
                                 yticks=np.arange(0, 600000, 100000))
gvutil.set_axes_limits_and_ticks(ax=ax2,
                                 xlim=(0, 21),
                                 ylim=(500000, 0),
                                 xticks=np.arange(0, 24, 3),
                                 yticks=np.arange(0, 600000, 100000))

# Remove ticklabels on Y axis for panel 2 (ax2)
ax2.yaxis.set_ticklabels([])

# Use geocat.viz.util convenience function to set titles without calling
# several matplotlib functions
gvutil.set_titles_and_labels(ax1, ylabel=T.z_t.long_name, labelfontsize=16)

# Manually set set titles and their positions
ax1.set_title(T.long_name, y=1.13, fontsize=16)
ax2.set_title(T.long_name, y=1.13, fontsize=16)

# Specify which contour levels to draw for panel 3 and panel 4
levels = np.arange(0, 28, 2)

# Import an NCL colormap
newcmp = gvcmaps.BlAqGrYeOrRe

# Panel 3: Contourf-plot data
T3.plot.contourf(ax=ax3,
                 levels=levels,
                 cmap=newcmp,
                 add_colorbar=False,
                 add_labels=False)

# Panel 4: Contourf-plot data
colors = T4.plot.contourf(ax=ax4,
                          levels=levels,
                          cmap=newcmp,
                          add_colorbar=False,
                          add_labels=False)

# Set y-axis to have log-scale
ax3.set_yscale('log')
ax4.set_yscale('log')
ax3.set_xscale('log')
ax4.set_xscale('log')

# Change formatter or else tick values will be in exponential form
ax3.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
ax4.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))

# Use geocat.viz.util convenience function to add minor and major ticks
gvutil.add_major_minor_ticks(ax3,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)
gvutil.add_major_minor_ticks(ax4,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax=ax3,
                                 ylim=(500000, 10000),
                                 xlim=(-90, 90),
                                 xticks=np.arange(-60, 91, 30),
                                 yticks=np.arange(400000, 99999, -100000))

#xticklabels=['60S', '30S', '0', '30N', "60N", "90N"]
gvutil.set_axes_limits_and_ticks(
    ax=ax4,
    ylim=(ax4.get_ylim()[::-1]),
    xlim=(-90, 90),
    xticks=np.arange(-60, 91, 30),
    #yticks=np.arange(100000, 500000, 100000)
)

# Set ticks on all sides of the plots
ax3.tick_params(which='both', top=True, right=True)
ax4.tick_params(which='both', top=True, right=True)

# Remove ticklabels on Y axis for panel 4
ax4.yaxis.set_ticklabels([])

# Use geocat.viz.util convenience function to set titles without calling
# several matplotlib functions
gvutil.set_titles_and_labels(ax3, ylabel=T.z_t.long_name, labelfontsize=16)

# Add colorbar
fig.colorbar(colors,
             ax=[ax1, ax2, ax3, ax4],
             orientation='horizontal',
             drawedges=True,
             extendrect=True,
             aspect=20,
             extendfrac='auto',
             pad=0.07,
             shrink=0.9,
             ticks=levels)

# Show the plot
plt.show()
