"""
NCL_conOncon_1.py
=================
This script illustrates the following concepts:
   - Drawing filled contours of zonal wind 
   - Changing the background color for contour labels
   - Drawing pressure and height scales
   - Using a Blue-White-Red colormap

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/h_lat_6.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/h_lat_6_lg.png
"""

################################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmap

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/mxclim.nc"))
# Extract variables
U = ds.U[0, :, :]
