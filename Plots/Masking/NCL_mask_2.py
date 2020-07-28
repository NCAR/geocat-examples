"""
NCL_mask_2.py
===============
This script illustrates the following concepts:
   - Using keyword zorder to mask areas in a plot
   - Drawing filled land areas on top of a contour plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/mask_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/mask_2_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
# Disable time decoding due to missing necessary metadata
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
# Extract a slice of the data at first time step
ds = ds.isel(time=0).drop("time")
TS = ds.TS
