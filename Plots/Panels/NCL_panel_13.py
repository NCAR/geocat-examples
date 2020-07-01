"""
NCL_panel_13.py
===============
This script illustrates the following concepts:
   - Overlaying a vector field over filled contours
   - Paneling two plots vertically

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_13.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_13_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import math

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))

# Extract data from second timestep
ds = ds.isel(time=1).drop_vars('time')
U = ds.U
V = ds.V

# Calculate the magnitude of the winds
speed = np.sqrt(U.data**2 + V.data**2)
