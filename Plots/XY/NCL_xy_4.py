"""
NCL_xy_4.py
===============
This script illustrates the following concepts:
   - Drawing a scatter plot
   - Changing the markers in an XY plot
   - Changing the marker color in an XY plot
   - Changing the marker size in an XY plot
   - Creating your own markers for an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_4.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_4_1_lg.png
                         https://www.ncl.ucar.edu/Applications/Images/xy_4_2_lg.png
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
ds = xr.open_dataset("../../../AtmJan360.nc", decode_times=False)
