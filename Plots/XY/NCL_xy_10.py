"""
NCL_xy_10.py
===============
This script illustrates the following concepts:
   - Filling the area between two curves in an XY plot
   - Drawing Greek characters on an XY plot
   - Controlling the draw order of a polygon

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_10.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_10_lg.png
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
ds = xr.open_dataset(gdf.get("netcdf_files/80.nc"))

# Extract slice of data
temp = ds.isel(time=0, drop=True).TS
