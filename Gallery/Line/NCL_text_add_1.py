"""
NCL_text_add_1.py
=================
This script illustrates the following concepts:
   - Adding text to a plot using plot data coordinates
   - Set the font size of text

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/text_add_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/text_1_lg.png
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

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
# Extract variables
uz = ds.U.isel(time=0, lon=8)
lon = ds.U.isel(time=0, lon=8).lat

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(6.5, 6.5))
ax = plt.gca()

# Plot data
plt.plot(lon, uz.values, c='gray', linewidth=0.9)

# Add text with set parameters
text_kwargs = dict(ha='center', va='center', fontsize=22.5, color='black')
plt.text(10, 0.0, 'Text in Plot Coordinates', **text_kwargs)

# Use geocat.viz.util convenience function to add minor and major tick lines
gv.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=5, labelsize=15)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, tick values, and tick labels to show latitude & longitude (i.e. North (N) - South (S))
gv.set_axes_limits_and_ticks(
    ax,
    xlim=(-90, 90),
    ylim=(-10, 40),
    xticks=np.linspace(-90, 90, 7),
    xticklabels=['90S', '60S', '30S', '0', '30N', '60N', '90N'],
)

# Use geocat.viz.util convenience function to set titles and labels
gv.set_titles_and_labels(ax, ylabel='Zonal Wind', labelfontsize=18)

# Show the plot
plt.tight_layout()
plt.show()
