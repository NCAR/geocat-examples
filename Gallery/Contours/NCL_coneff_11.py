"""
NCL_coneff_11.py
================
This script illustrates the following concepts:
   - Filling contours with multiple shaded patterns
   - Filling contours with stippling (solid dots)
   - Changing the size of the dot fill pattern in a contour plot
   - Overlaying a stipple pattern to show area of interest
   - Changing the density of contour shaded patterns

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/coneff_11.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/coneff_11_1_lg.png
                          https://www.ncl.ucar.edu/Applications/Images/coneff_11_2_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cmaps

import geocat.datafiles as gdf
import geocat.viz as gv

###############################################################################
# Read in data

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/atmos.nc'), decode_times=False)

# Select meridional wind at lowest level
v = ds.V.isel(time=0, lev=0)

###############################################################################
