"""
NCL_h_lat_7.py
==============
This script illustrates the following concepts:
   - Drawing filled contours of zonal wind
   - Changing the background color for contour labels
   - Drawing pressure and height scales
   - Using a Blue-White-Red colormap

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/h_lat_7.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/h_lat_7_lg.png
"""

###############################################################################
# Import packages:

import xarray as xr
from matplotlib import pyplot as plt
import numpy as np

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.comp import interp_hybrid_to_pressure

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)

# Extract variables
T = ds.T  # temperature (K)
V = ds.V  # meridional wind (m/s)
Z = ds.Z3  # geopotl. height in m
omega = ds.OMEGA  # vert. pres. vel.(mb/day)
lev = ds.lev  # pressure levels (millibars)
q = ds.Q  # spec. humidity (g/kg)
q = q / 1000  # change units to kg/kg
lev = 100 * lev  # change units to Pa

################################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 11.5))

# Generate axes
ax = plt.axes()

# Specify which contours should be drawn
levels = np.linspace(-55, 55, 23)

plt.tight_layout()
plt.show()
