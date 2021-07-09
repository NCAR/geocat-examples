"""
NCL_time_labels_1.py
====================
This script illustrates the following concepts:
   - Labeling the X axis with nicely-formatted time labels
   - Setting the precision of tickmark labels
   - Generating dummy data using numpy's random.uniform
   - Removing trailing zeros from tickmark labels
   - Setting the mininum/maximum value of the X axis in an XY plot
   - Changing the width and height of a plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/time_labels_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/time_labels_1_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from geocat.viz import util as gvutil

###############################################################################
# Generate date data:

tstart = 2000
tend = 2006
t_size = (tend - tstart + 1) * 12

# Create an array of years from tstart to tend in fractional format
# This has the same effect as NCL functions yyyymm_time() and yyyymm_to_yyyyfrac()
date = np.empty(t_size)
i = 0
for year in range(tstart, tend + 1):
    for mo in range(1, 13):  # Loop through all the months
        date[i] = year + (mo - 1) / 12
        i += 1

# Create random 1D array
arr = np.random.uniform(-5., 10., t_size)

###############################################################################
# Plot 1: Display years in fractional format

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(1, figsize=(8, 3.5))
ax = plt.axes()

# Plot data
plt.plot(date, arr, color='gray', linewidth=0.5)

# format ytick labels
ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=5,
                             y_minor_per_major=3,
                             labelsize=14)

# Usa geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(tstart, tend + 1),
                                 ylim=(-6, 12),
                                 yticks=np.arange(-6, 13, 3))

# Set spacing between tick labels and axes
ax.tick_params('both', pad=9)

# Draw plot on the screen
plt.tight_layout()
plt.show()

###############################################################################
# Plot 2: Display years in integer format (remove trailing zeros)

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(2, figsize=(8, 4))
ax = plt.axes()

# Plot data
plt.plot(date, arr, color='gray', linewidth=0.5)

# format ytick labels
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=5,
                             y_minor_per_major=3,
                             labelsize=14)

# Usa geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(tstart, tend + 1),
                                 ylim=(-6, 12),
                                 yticks=np.arange(-6, 13, 3))

# Set spacing between tick labels and axes
ax.tick_params('both', pad=9)

# Add maintitle
ax.set_title('time', fontsize=16, y=1.04)

# Draw plot on the screen
plt.tight_layout()
plt.show()

###############################################################################
# Plot 3: Display both months and years

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(2, figsize=(8, 4))
ax = plt.axes()

# Plot the first 13 timestamps of the data
plt.plot(date[0:13], arr[0:13], color='gray', linewidth=0.5)

# format ytick labels
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=1,
                             y_minor_per_major=4,
                             labelsize=14)

# Usa geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(date[0], date[12]),
                                 ylim=(-4, 10),
                                 xticks=date[0:13],
                                 xticklabels=[
                                     'Jan\n2000', "Feb\n2000", "Mar\n2000",
                                     "Apr\n2000", "May\n2000", "Jun\n2000",
                                     "Jul\n2000", " Aug\n2000", " Sep\n2000",
                                     " Oct\n2000", " Nov\n2000", " Dec\n2000",
                                     " Jan\n2001"
                                 ],
                                 yticks=np.arange(-4, 11, 2))

# Set spacing between tick labels and axes
ax.tick_params('both', pad=9)

# Add maintitle
ax.set_title('time', fontsize=16, y=1.04)

# Draw plot on the screen
plt.tight_layout()
plt.show()
