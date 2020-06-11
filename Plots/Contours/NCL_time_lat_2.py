"""
NCL_time_lat_2.py
===============

This script illustrates the following concept:
   - Creating a time vs latitude plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://ncl.ucar.edu/Applications/Scripts/time_lat_2.ncl
    - Original NCL plot: https://ncl.ucar.edu/Applications/Images/time_lat_2_sm.png
    - https://ncl.ucar.edu/Applications/time_lat.shtml

"""

###############################################################################
# Import packages
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from cartopy.mpl.ticker import LatitudeFormatter

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil


###############################################################################
# Read in our data

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/b003_TS_200-299.nc'), decode_times=False)
ts = ds.TS[:, :, 29]

###############################################################################
# Create our plot

# Import an NCL colormap
palette = gvcmaps.ViBlGrWhYeOrRe

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(7, 7))

# Create axes
ax = plt.axes()

# Contourf-plot data
heatmap = ts.plot.contourf(ax=ax, levels=25, vmin=195, vmax=315, cmap=palette, add_colorbar=False)

# Add colorbar
cbar = plt.colorbar(heatmap, fraction=.1, ticks=np.arange(195, 320, 5), drawedges=True)
cbar.ax.set_yticklabels([str(i) if i % 10 == 0 else '' for i in np.arange(195, 315, 5)])
cbar.ax.tick_params(size=0)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax, maintitle="color example", maintitlefontsize=16,
                                 lefttitle="Surface Temperature", lefttitlefontsize=14,
                                 righttitle="K", righttitlefontsize=14, xlabel="", ylabel="time")
# Adjust height of the title so it's on screen
ax.set_title("color example", fontsize=16, y=1.1)

# Use a geocat.viz.util convenience function to set xticks and labels
xtick_labs = [str(abs(i))+('S' if i < 0 else 'N') if i % 10 != 0 else '' for i in np.arange(-75, 80, 15)]
gvutil.set_axes_limits_and_ticks(ax, xticks=np.arange(-75, 80, 15), xticklabels=xtick_labs)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=5, labelsize=12)

# Show the plot
plt.show()
