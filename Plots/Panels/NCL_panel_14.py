"""
NCL_panel_14.py
===============
This script illustrates the following concepts:
   - Combining two sets of paneled plots on one page
   - Adding a common labelbar to paneled plots
   - Reversing the Y axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_14.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_14_lg.png
"""

##############################################################################
# Import packages:

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"),
                     decode_times=False)
# Ensure longitudes range from 0 to 360 degrees
T = gvutil.xr_add_cyclic_longitudes(ds.T, "lon_t")

##############################################################################
# Plot:
fig = plt.figure(figsize=(10, 10))

grid = gridspec.GridSpec(nrows=2, ncols=2, figure=fig)

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(grid[0])  # upper left cell of grid
ax2 = fig.add_subplot(grid[1])  # upper right cell of grid
ax3 = fig.add_subplot(grid[2], projection=proj)  # lower left cell of grid
ax4 = fig.add_subplot(grid[3], projection=proj)  # lower right cell of grid

print(T.isel(time=0, lat_t=-30, lon_t=180))

# Plot xy data at upper left and right plots
ax1.plot(
    T.isel(time=0).sel(lat_t=slice(30), lon_t=slice(180)),
    #T.z_t,
    c='black',
    linewidth=0.5)
ax2.plot(
    T.isel(time=0).isel(lat_t=slice(-30), lon_t=slice(180)),
    #T.z_t,
    c='black',
    linewidth=0.5)

# Show the plot
plt.show()
