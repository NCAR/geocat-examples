"""
NCL_dev_2.py
===============
This script illustrates the following concepts:
   - Calculating deviation from zonal mean
   - Drawing zonal average plots
   - Moving the contour informational label into the plot
   - Changing the background color of the contour line labels
   - Spanning part of a color map for contour fill
   - Making the colorbar be vertical
   - Paneling four subplots in a two by two grid using `gridspec`
   - Changing the aspect ratio of a subplot
   - Drawing color-filled contours over a cylindrical equidistant map
   - Using a blue-white-red color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/dev_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/dev_2_lg.png
"""

##############################################################################
# Import packages:
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
                     decode_times=False)

# Extract slice of data
TS = ds.TS.isel(time=0).drop('time')

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
TS = gvutil.xr_add_cyclic_longitudes(TS, "lon")

# Calculate zonal mean
mean = TS.mean(dim='lon')

# Using meshgrid, a 2-D array can be created with the same shape as the
# temperature data with the zonal mean for each latitude filling each row.
# This way we can subtract each element of the mean 2-D array from the
# corresponding element in the data array.
waste, mean_grid = np.meshgrid(TS['lon'], mean)

# Calculate deviations from zonal mean
dev = TS.data - mean_grid
