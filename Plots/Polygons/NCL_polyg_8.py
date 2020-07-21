"""
NCL_polyg_8.py
==============
This script illustrates the following concepts:
   - Drawing a scatter plot on a map
   - Changing the marker color and size in a map plot
   - Plotting station locations using markers
   - Manually creating a legend using markers and text
   - Adding text to a plot
   - Generating dummy data using "random_uniform"
   - Binning data

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polyg_8.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polyg_8_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from geocat.viz import util as gvutil

###############################################################################
# Generate dummy data
npts = 100
random = np.random.default_rng(seed=1)
# Create random coordinates to position the markers
lat = random.uniform(low=25, high=50, size=npts)
lon = random.uniform(low=235, high=290, size=npts)
# Create random data which the color will be based off of
r = random.uniform(low=-1.2, high=35, size=npts)

bins = [0, 5, 10, 15, 20, 23, 26]
colors = ['mediumpurple', 'blue', 'cyan', 'green', 'limegreen', 'greenyellow',
          'yellow', 'orange']