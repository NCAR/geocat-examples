"""
NCL_lb_3.py
===============
This script illustrates the following concepts:
   - Changing the colorbar labels
   - Changing the angle of colorbar labels
   - Adding a title to a colorbar
   - Changing the font size of the colorbar's labels
   - Moving the colorbar away from the plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lb_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lb_3_lg.png
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
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
# Extract variable
V = ds.V.isel(time=0, lev = 3)

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
V = gvutil.xr_add_cyclic_longitudes(V, "lon")
