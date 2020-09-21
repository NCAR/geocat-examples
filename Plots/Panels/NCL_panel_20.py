"""
NCL_panel_20.py
===============
This script illustrates the following concepts:
   - Drawing four different-sized plots on the same page using gridspec

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_20.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_20_lg.png

"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))

# Extract data from second timestep
ds = ds.isel(time=1).drop_vars('time')

# Ensure longitudes range from 0 to 360 degrees
U = gvutil.xr_add_cyclic_longitudes(ds.U, "lon")
V = gvutil.xr_add_cyclic_longitudes(ds.V, "lon")
