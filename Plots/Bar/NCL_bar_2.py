"""
NCL_bar_2.py
===============
This script illustrates the following concepts:
   - Drawing bars instead of curves in an XY plot
   - Changing the aspect ratio of a bar plot
   - Drawing filled bars up or down based on a Y reference value
   - Setting the minimum/maximum value of the Y axis in a bar plot
   - Using named colors to indicate a fill color
   - Creating array of dates to use as x-axis tick labels
   - Creating a main title

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/bar_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/soi.nc"))
dsoik = ds.DSOI_KET
dsoid = ds.DSOI_DEC
date = ds.date

# Creating a new array for x axis labels
datedim = np.shape(date)[0]
new_date = np.empty_like(date)
# Dates in the file are represented by year and month
# Create array that represents data by year and months as a fraction of a year
for n in np.arange(0, datedim, 1):
    yyyy = date[n]/100
    mon = date[n]-yyyy*100
    new_date[n] = yyyy + (mon-1)/12
