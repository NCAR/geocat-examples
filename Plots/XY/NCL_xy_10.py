"""
NCL_xy_10.py
===============
This script illustrates the following concepts:
   - Filling the area between two curves in an XY plot
   - Drawing Greek characters on an XY plot
   - Controlling the draw order of a polygon

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_10.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_10_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/80.nc"))
# Extract slice of data
TS = ds.isel(time=0, lon=21, drop=True).TS

###############################################################################
# Plot:
plt.figure(figsize=(8,8))
ax = plt.axes()

TS.plot.line(ax=ax, color='black', _labels=False)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=4,
                             labelsize=14)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(220, 320), xlim=(-90, 90),
                                 xticks=np.arange(-90, 91, 30))

plt.show()
