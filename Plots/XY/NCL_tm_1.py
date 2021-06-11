"""
NCL_tm_1.py
===========

Note: This script is aimed at demonstrating the explicit handling of tick marks, their locations, labels, etc.;
therefore, the use of geocat-viz convenience functions is minimized here to show such tick management functions directly
throughout this script.

This script illustrates the following concepts:
   - Setting the mininum/maximum value of the Y axis in an XY plot
   - Changing the width and height of a plot
   - Forcing a tickmark label at beginning of X axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/tm_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/tm_1_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/tm_1_2_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FixedLocator, FormatStrFormatter

from geocat.viz import util as gvutil

###############################################################################
# Generate data:

# Note that range() top value is not included in the returned array of values.
x_data = np.arange(1950, 2006)
nyears = x_data.size
y_data = np.random.uniform(-4, 4, nyears)

# Print out a formatted message; note the starting 'f' for the string.
print(
    f"There are { len(x_data) } values in x_data, and { len(y_data) } values in y_data."
)

###############################################################################
# Plot 1

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(1, figsize=(8, 3.5))
ax = plt.gca()

# Format the tick labels. Use integers for the major ticks.
# For the minor ticks, use no labels; defaults to NullFormatter.
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Set the major tick spacing.
major_tick_spacing = 10
ax.xaxis.set_major_locator(MultipleLocator(major_tick_spacing))

# Draw ticks on all sides of the plot.
plt.tick_params(which='both', top=True, right=True)

# Increase the length of the tick marks.
plt.tick_params(which='major', length=10.0, width=0.5)
plt.tick_params(which='minor', length=5.0, width=0.25)

# Set label size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set the minor tick spacing for X and Y axes.
ax.xaxis.set_minor_locator(MultipleLocator(2))
ax.yaxis.set_minor_locator(MultipleLocator(0.5))

# Plot data and set the X axis limits.
plt.plot(x_data, y_data, color='grey', linewidth=0.5)

# Usa geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(min(x_data) - 1, max(x_data) + 1),
                                 ylim=(-4.5, 4.5))

# Draw plot on the screen
plt.tight_layout()
plt.show()

###############################################################################
# Plot 2 (forced tickmark label at the beginning of X axis)

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(2, figsize=(8, 3.5))
ax = plt.gca()

# Format the tick labels.
# For the minor ticks, use no labels; defaults to NullFormatter.
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Set the major tick spacing.
major_tick_spacing = 10
xticks = [1949, 1959, 1969, 1979, 1989, 1999]
ax.xaxis.set_major_locator(FixedLocator(xticks))

# Draw ticks on all sides of the plot.
plt.tick_params(which='both', top=True, right=True)

# Increase the length of the tick marks.
plt.tick_params(which='major', length=10.0, width=0.5)
plt.tick_params(which='minor', length=5.0, width=0.25)

# Set label size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set the minor tick spacing for X and Y axes.
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(MultipleLocator(0.5))

# Line-plot data
plt.plot(x_data, y_data, color='grey', linewidth=0.5)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, and tick values on x-axes.
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(min(x_data) - 1, max(x_data) + 1),
                                 ylim=(-4.5, 4.5))

# Draw plot on the screen
plt.tight_layout()
plt.show()
