"""
NCL_sat_1.py
===============
This script illustrates the following concepts:
   - Using 'short2flt' to unpack 'short' data
   - Drawing line contours over a satellite map
   - Changing the view of a satellite map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"))

print(ds)

###############################################################################
# Create plot

plt.figure(figsize=(10, 10))
m = Basemap(projection='ortho', resolution=None, lat_0=50, lon_0=-100)