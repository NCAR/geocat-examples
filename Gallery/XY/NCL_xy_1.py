"""
NCL_xy_1.py
===========
This script illustrates the following concepts:
    - Drawing a black and white XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_1_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load data into xarray
data = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
U = data.U

###############################################################################
# Plot:

# Create figure (setting figure size (width,height) in inches) and axes
plt.figure(figsize=(7, 6.5))
ax = plt.gca()

# Plot the specific slice of the data with the correct color and linewidth
U.isel(time=0).sel(lon=82, method='nearest').plot(
    x="lat", color="#afafaf", linewidth=1.1
)

# Use geocat.viz.util convenience function to add minor and major tick lines
gv.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=5, labelsize=16)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, tick values, and tick labels to show latitude & longitude (i.e. North (N) - South (S))
gv.set_axes_limits_and_ticks(
    ax,
    xlim=(-90, 90),
    ylim=(-10, 50),
    xticks=np.linspace(-90, 90, 7),
    yticks=np.linspace(-10, 50, 7),
    xticklabels=['90S', '60S', '30S', '0', '30N', '60N', '90N'],
)

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gv.set_titles_and_labels(ax, maintitle="Basic XY plot", xlabel="", ylabel="Zonal Wind")

# Show the plot
plt.tight_layout()
plt.show()
