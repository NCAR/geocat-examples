"""
NCL_xy_16.py
===============
This script illustrates the following concepts:
   - Drawing a legend inside an XY plot
   - Drawing an X reference line in an XY plot
   - Reversing the Y axis
   - Using log scaling and explicit labeling
   - Changing the labels in a legend
   - Creating a vertical profile plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_16.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_16_1_lg.png
                         https://www.ncl.ucar.edu/Applications/Images/xy_16_2_lg.png
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
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
U = ds.U.isel(time=0).drop('time').isel(lon=0).drop('lon')
print(U)
# Extract slices of the data at different latitudes
U20 = U.where(U.lat==20)
U30 = U.where(U.lat==30)
U40 = U.where(U.lat==40)
U50 = U.where(U.lat==50)