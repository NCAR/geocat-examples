"""
NCL_station_1.py
================
This script illustrates the following concepts:
   - Using pandas package to read in ascii file
   - Contouring one-dimensional X, Y, Z data
   - Reading an ASCII file with several columns of data
   - Drawing lat/lon locations as filled dots using gsn_coordinates
   - Controlling which contour lines get drawn
   - Using opacity to emphasize or subdue overlain features
   - Reversing a color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/station_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/station_1_lg.png
"""

###################################################
# Import packages:

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import pandas as pd
import cartopy
import cartopy.crs as ccrs

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###################################################
# Generate data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = pd.read_csv(gdf.get('ascii_files/pw.dat'), delimiter='\\s+')

# Extract columns
pwv = ds.PW
pwv_lat1d = ds.LAT
pwv_lon1d = ds.LON

###################################################
# Plot

#
fig = plt.figure(figsize=(9, 9))

#
ax = plt.axes()

# Plot filled contours

# Show the plot
plt.show()
