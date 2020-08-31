"""
NCL_panel_10.py
===============
This script illustrates the following concepts:
   - Drawing Hovmueller plots
   - Attaching plots along the Y axis
   - Using a blue-white-red color map
   - Drawing zonal average plots
   - Paneling attached plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_10.ncl and https://www.ncl.ucar.edu/Applications/Scripts/panel_attach_10.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_10_lg.png and https://www.ncl.ucar.edu/Applications/Images/panel_attach_10_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/chi200_ud_smooth.nc"))
chi = ds.CHI

# Scale the data for convenience
scale = 1e6
chi = chi / scale

##############################################################################
# Creat Single Plot:
fig, (ax1, ax2) = plt.subplots(nrows=1,
                               ncols=2,
                               sharey=True,
                               figsize=(12, 9),
                               gridspec_kw=dict(wspace=0,
                                                width_ratios=[0.75, 0.25]))
# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax=ax1,
                                 xlim=(100, 215),
                                 ylim=(0, 180),
                                 xticks=(135, 180),
                                 yticks=np.arange(0, 181, 30),
                                 xticklabels=('135E', '180'))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax=ax1)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax=ax2,
                                 xlim=(-0.6, 0.9),
                                 ylim=(0, 180),
                                 xticks=np.arange(-0.3, 0.9, 0.3),
                                 yticks=np.arange(0, 181, 30))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax=ax2, x_minor_per_major=1)

plt.show()
