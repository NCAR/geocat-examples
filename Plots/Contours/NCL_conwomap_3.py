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
# Generate random 2D data

###############################################################################
#create figure
plt.figure(figsize=(10,10))

#create axes
ax = plt.axes()
ax.set_aspect(1.5)

gvutil.set_axes_limits_and_ticks(ax, xlim=(0, 30), ylim=(0, 30), xticks=None, yticks=None, xticklabels=None, yticklabels=None)

x = []

for i in range(0, 30+1):
    x.append(i)

x = np.array(x)

plt.step(x, x)

plt.show()