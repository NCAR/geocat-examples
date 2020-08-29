"""
NCL_panel_10.py
===============
This script illustrates the following concepts:
   - Drawing Hovmueller plots
   - Attaching plots along the Y axis
   - Using a blue-white-red color map
   - Drawing zonal average plots
   - Paneling attached plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_10.ncl and https://www.ncl.ucar.edu/Applications/Scripts/panel_attach_10.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_10_lg.png and https://www.ncl.ucar.edu/Applications/Images/panel_attach_10_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays, choosing the 2nd timestamp
ds = xr.open_dataset(gdf.get("netcdf_files/chi200_ud_smooth.nc"))
