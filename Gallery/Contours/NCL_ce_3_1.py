"""
NCL_ce_3_1.py
=============

This script illustrates the following concepts:
   - Drawing color-filled contours over a cylindrical equi-distant map
   - Changing the contour level spacing
   - Turning off contour lines
   - Zooming in on a particular area on the map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/ce_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/ce_3_1_lg.png

.. Warning::
    This is an experimental version of the script. Go to the [latest](https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_ce_3_1.html) version for the stable version.

    See the geocat-viz experimental documentation for the functionality in this script [here](https://geocat-viz.readthedocs.io/en/experimental/).
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.datafiles as gdf
import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarray
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'),
                     decode_times=False)

# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0).sel(lat_t=slice(-60, 30), lon_t=slice(30, 120))

###############################################################################
# Plot:

# Use geocat.viz utility function to create a contour plot
plot_ = gv.Contour(
    t,  # data
    w=10,  # width of plot
    h=8,  # height of plot
    contour_lines=False,
    xlim=(30, 120),
    ylim=(-60, 30),
    cb_orientation="vertical",  # orientation of colorbar
    cb_tick_labels=np.arange(0, 32, 2),  # colorbar tick labels
    cb_ticks=np.arange(0, 32, 2),  # colorbar tick locations
    levels=np.linspace(0, 31, 40),  # contour levels
    main_title_fontsize=23,
    left_title_fontsize=23,
    right_title_fontsize=23,
    land_on=True,  # Show land on plot
    main_title="30-degree major and 10-degree minor ticks")

# Additional formatting
# Get current axis
ax = plt.gca()

# Customize tick length and width
ax.tick_params(axis='both', which='minor', length=5, width=0.8)
ax.tick_params(axis='both', which='major', length=12, width=1)

# Remove degree symbol from tick labels
ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# Show the plot
plot_.show()
