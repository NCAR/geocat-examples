"""
NCL_panel_35.py
===============
This script illustrates the following concepts:
   - Attaching three filled contour plots along Y axes
   - Adding a common labelbar to attached plots
   - Adding a common title to attached plots
   - Generating dummy data using "numpy.rand" and "signal.convolve"
   - Drawing a custom labelbar
   - Drawing a custom title
   - Retrieving the bounding box of a plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_35.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_35_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np

from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

from scipy import signal
###############################################################################
# Create figure and axes using gvutil
plt.figure()
fig, axs = plt.subplots(1, 3, figsize=(12, 6), sharex='all', sharey='all', gridspec_kw={'wspace': 0})

gvutil.set_axes_limits_and_ticks(axs[0], xticks=np.arange(0, 120, 20), yticks=np.arange(0, 120, 20), xticklabels=np.arange(0, 100, 20), yticklabels=np.arange(0, 100, 20))
gvutil.add_major_minor_ticks(axs[0], x_minor_per_major=4, y_minor_per_major=4)
axs[0].tick_params(axis='both', which='both', top=True, left=True, right=False)
axs[0].set_aspect(aspect='equal')

gvutil.set_axes_limits_and_ticks(axs[1], xticks=np.arange(0, 120, 20), yticks=np.arange(0, 120, 20), xticklabels=np.arange(0, 100, 20), yticklabels=np.arange(0, 100, 20))
gvutil.add_major_minor_ticks(axs[1], x_minor_per_major=4, y_minor_per_major=4)
axs[1].tick_params(axis='both', which='both', top=True, left=False, right=False)
axs[1].set_aspect(aspect='equal')

gvutil.set_axes_limits_and_ticks(axs[2], xticks=np.arange(0, 120, 20), yticks=np.arange(0, 120, 20), xticklabels=np.arange(0, 100, 20), yticklabels=np.arange(0, 100, 20))
gvutil.add_major_minor_ticks(axs[2], x_minor_per_major=4, y_minor_per_major=4)
axs[2].tick_params(axis='both', which='both', top=True, left=False, right=True)
axs[2].set_aspect(aspect='equal')

# Create dummy data
nx = 100
ny = 100
rand1 = np.random.rand(nx, ny)
x, y = np.meshgrid(np.arange(0, 100), np.arange(0, 100))
scale = 0.01
filter = scale*np.exp(np.sin(x)+np.cos(y))
a = signal.convolve(rand1, filter, mode='same')

filter = scale*np.exp(np.sin(x)*np.sin(y))
b = signal.convolve(rand1, filter, mode='same')

filter = scale*np.exp(np.sin(y))
c = signal.convolve(rand1, filter, mode='same')

# Plot data and create colorbar
newcmap = gvcmaps.BlueYellowRed
p = axs[0].contourf(x, y, a, cmap=newcmap, levels=12)
axs[0].contour(p, colors='k', linestyles='solid', linewidths=0.5)
p = axs[1].contourf(x, y, b, cmap=newcmap, levels=12)
axs[1].contour(p, colors='k', linestyles='solid', linewidths=0.5)
p = axs[2].contourf(x, y, c, cmap=newcmap, levels=12)
axs[2].contour(p, colors='k', linestyles='solid', linewidths=0.5)

cbar = fig.colorbar(p, orientation='horizontal', ax=axs, ticks=np.arange(20, 85, 5), shrink=0.75)

# Add title
fig.suptitle("Three dummy plots attached along Y axes", fontsize=18, fontweight='bold')

# Get bounding box
bbox = fig.get_window_extent()

plt.show()
