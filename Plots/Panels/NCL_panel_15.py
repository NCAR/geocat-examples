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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
print(t_1, t_2, t_6)