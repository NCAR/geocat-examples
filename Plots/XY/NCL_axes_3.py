"""
NCL_axes_3.py
=============
This script illustrates the following concepts:
   - Removing the border, tickmarks, and labels from an XY plot
   - Drawing vertical grid lines on an XY plot
   - Making an axis logarithmic in an XY plot
   - Drawing four XY plots in the same figure using matplotlib.subplots
   - Drawing Y axis labels using exponents

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/axes_3.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/axes_3_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Create dummy data for XY plots

npts = 500

x = 500 + 0.9 * np.arange(0, npts) * np.cos(np.pi/100 * np.arange(0, npts))
y = 500 + 0.9 * np.arange(0, npts) * np.sin(np.pi/100 * np.arange(0, npts))

###############################################################################
# Plot:

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 10), gridspec_kw=dict(wspace=0.5, hspace=0.5))

# Create plot with linear axes and full perimeter
axes[0][0].plot(x, y)

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(axes[0][0],
                             maintitle="Perimeter Background",
                             xlabel="Linear",
                             ylabel="Linear")

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axes[0][0],
                             x_minor_per_major=2,
                             y_minor_per_major=2,
                             labelsize=10)

# Use geocat.viz.util convenience function to set axes limits and tick labels
gvutil.set_axes_limits_and_ticks(axes[0][0],
                                 xlim=(0, 900),
                                 ylim=(100, 1000),
                                 xticks=range(0, 901, 100),
                                 yticks=range(100, 1001, 100))


# Create plot with log y-axis and gridlines
axes[0][1].set_yscale('log')
axes[0][1].plot(x, y)

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(axes[0][1],
                             maintitle="Grid Background",
                             xlabel="Linear",
                             ylabel="Logarithmic")

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axes[0][1],
                             x_minor_per_major=2,
                             y_minor_per_major=2,
                             labelsize=10)

# Use geocat.viz.util convenience function to set axes limits and tick labels
gvutil.set_axes_limits_and_ticks(axes[0][1],
                                 xlim=(0, 900),
                                 ylim=(100, 1000),
                                 xticks=range(0, 901, 100))

# Remove labels for minor ticks on log scale
axes[0][1].yaxis.set_minor_formatter(NullFormatter())

# Turn on vertical gridlines
axes[0][1].grid(True, which='major', axis='x', color='black')

plt.show()
