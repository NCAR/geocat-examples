"""
NCL_panel_15.py
===============
This script illustrates the following concepts:
   - Paneling two sets of paneled plots on one figure
   - Using nested `gridspec` objects to make a more complex panelled plot 

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_15.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_15_lg.png
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
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil
##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

# Selecting the first time step and then the three levels of interest
t = ds.T.isel(time=0)
t_1 = t.isel(z_t=0)
t_2 = t.isel(z_t=1)
t_6 = t.isel(z_t=5)

##############################################################################
# Plot:

"""
The outer gridspec will be a 2x2 grid with the top row having a height that
is two thirds of the figure height. The bottom row will have a height that is
one third of the figure height. The right column will be just thick enough to
accommodate the color bars.
"""
fig = plt.figure(figsize=(7, 15))

outer_grid = gridspec.GridSpec(nrows=2,
                               ncols=2,
                               figure=fig,
                               height_ratios=[2/3, 1/3],
                               width_ratios=[0.95, 0.05])

"""
The inner gridspec will be nested in the top, left cell of the outer gridspec.
This inner gridspec will have two rows and one column to accommodate the
stacked plots that will share a colorbar.
"""
inner_grid = gridspec.GridSpecFromSubplotSpec(nrows=2,
                                              ncols=1,
                                              subplot_spec=outer_grid[0])

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(inner_grid[0], projection=proj) # upper cell of inner grid
ax2 = fig.add_subplot(inner_grid[1], projection=proj) # lower cell of inner grid
cax1 = fig.add_subplot(outer_grid[1]) # upper right cell of outer grid, for top color bar
ax3 = fig.add_subplot(outer_grid[2], projection=proj) # bottom left cell of outer grid
cax1 = fig.add_subplot(outer_grid[3]) # bottom right cell of outer grid, for bottom color bar

plt.show()