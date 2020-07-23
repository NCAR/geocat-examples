"""
NCL_xy_12.py
===============
This script illustrates the following concepts:
   - Emphasizing part of a curve in an XY plot
   - Drawing longitude labels on the X axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_12.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_12_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/xy_12_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import math

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))

# Extract slice of data
U = ds.isel(time=0, drop=True).U
