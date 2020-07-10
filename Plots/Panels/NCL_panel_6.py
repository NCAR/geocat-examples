"""
NCL_panel_6.py
===============
This script illustrates the following concepts:
   - Paneling four plots on a page
   - Adding white space aroudn paneled plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_6.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_6_lg.png
        https://www.ncl.ucar.edu/Applications/Images/panel_6_2_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays, choosing the 2nd timestamp
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

data0 = ds.T.isel(time=0, drop=True).isel(z_t=0, drop=True)
data1 = ds.T.isel(time=0, drop=True).isel(z_t=5, drop=True)
data2 = ds.S.isel(time=0, drop=True).isel(z_t=0, drop=True)
data3 = ds.S.isel(time=0, drop=True).isel(z_t=3, drop=True)

data0 = gvutil.xr_add_cyclic_longitudes(data0, "lon_t")
data1 = gvutil.xr_add_cyclic_longitudes(data1, "lon_t")
data2 = gvutil.xr_add_cyclic_longitudes(data2, "lon_t")
data3 = gvutil.xr_add_cyclic_longitudes(data3, "lon_t")

data = [[data0, data1], [data2, data3]]
