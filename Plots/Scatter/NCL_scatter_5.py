"""
NCL_scatter_5.py
================
This script illustrates the following concepts:
   - Drawing a scatter plot with markers of different colors
   - Generating dummy data using "random_normal"
   - Drawing a legend outside an XY plot
   - Changing the markers in an XY plot
   - Changing the marker color in an XY plot
   - Changing the marker size in an XY plot
   - Manually creating a legend using markers and text
   - Adding text to a plot
   - Creating a color map using named colors
   - Moving a legend closer to a plot
   - Customizing the labels in a legend
   - Changing the orientation of a legend

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/scatter_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/scatter_5_lg.png
"""

################################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

################################################################################
# Generate random data with an average of 10 and a stddev of 3
npts = 300
random = np.random.default_rng()
data = random.normal(loc=10, scale=3, size=npts)

plt.scatter(range(0, npts), data)
plt.show()