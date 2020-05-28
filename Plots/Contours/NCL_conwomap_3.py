"""
NCL_conwomap_3.py
=================
Concepts illustrated:
  - Drawing a simple contour plot
  - Generating dummy data using "random_normal"
  - Masking mirrored contour data
  - Drawing a perimeter around areas on a contour plot with missing data
  - Turning off the bottom and right borders of a contour plot
  - Using "getvalues" to retrieve resource values
  - Changing the labels and tickmarks on a contour plot
  - Adding a complex Greek character to a contour plot
  - Moving the contour informational label into the plot
  - Forcing tickmarks and labels to be drawn on the top X axis in a contour plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conwomap_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conwomap_3_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Generate random data:

xlist = np.linspace(0, 30.0, 50)
ylist = np.linspace(0, 30.0, 50)
xdata, ydata = np.meshgrid(xlist, ylist)

zdata = np.random.normal(20, 10, size=(50, 50))

###############################################################################
#create figure
plt.figure(figsize=(10,10))

#create axes
ax = plt.axes()

# Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(ax, xlim=(0, 30), ylim=(0, 30), xticks=None, yticks=None, xticklabels=None, yticklabels=None)

# Use geocat.viz.util to add major and minor tics
gvutil.add_major_minor_ticks(ax, x_minor_per_major=4, y_minor_per_major=4)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, ylabel="wave number", labelfontsize=18)

#create a numpy array of 30
x = np.arange(0,31)

#plot a step function
plt.step(x, x)

#Create boundary functions for fill
y1 = np.full(shape=31, fill_value=0, dtype=np.int)
y2 = x

#Plot contour data
cp = ax.contour(xdata, ydata, zdata, colors='k', linewidths=1.0)

#Label contours
ax.clabel(cp, inline=True, fontsize=10, colors='k', fmt="%.0f")

#Ignore second half of the graph
ax.fill_between(x, y1, y2, where=y2 >= y1, color='white', step='pre', alpha=1.0, zorder=4)

# these are matplotlib.patch.Patch properties
props1 = dict(facecolor='white', edgecolor = 'white', alpha=0.5)
props2 = dict(facecolor='white', edgecolor='black', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.70, 0.35, 'J(\u03B1)', transform=ax.transAxes, fontsize=20,
        bbox=props1, zorder=5)

# place a text box in upper left in axes coords
ax.text(0.70, 0.05, 'CONTOUR FROM -8 TO 6 BY 1', transform=ax.transAxes, fontsize=10,
         bbox=props2, zorder=5)

plt.show()