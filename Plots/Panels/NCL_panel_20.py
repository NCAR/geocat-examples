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
import matplotlib.gridspec as gridspec
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

###############################################################################
# Plot:
fig = plt.figure(figsize=(8, 7))

grid = gridspec.GridSpec(nrows=2,
                         ncols=2,
                         height_ratios=[0.6, 0.4],
                         figure=fig)

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(grid[0], aspect=1)  # upper left cell of grid
ax2 = fig.add_subplot(grid[1], aspect=1)  # upper right cell of grid
ax3 = fig.add_subplot(grid[2], projection=proj) # lower left cell of grid
ax4 = fig.add_subplot(grid[3], projection=proj) # lower right cell of grid

plt.show()
