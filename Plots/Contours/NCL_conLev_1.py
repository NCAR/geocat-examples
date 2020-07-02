"""
NCL_conLev_1.py
===============
This script illustrates the following concepts:
   - Explicitly setting contour levels
   - Drawing contour lines over a cylindrical equidistant map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conLev_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conLev_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"), decode_times=False)
# Extract slice of the data
temp = ds.TS.isel(time=43).drop_vars(names=['time'])
