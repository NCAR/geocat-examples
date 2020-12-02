"""
NCL_xy_19.py
============
This script illustrates the following concepts:
   - Drawing an XY plot with three different Y axes
   - Drawing a custom legend inside an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_19.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_19_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/xy_19_2_lg.png and https://www.ncl.ucar.edu/Applications/Images/xy_19_3_lg.png

"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

################################################################################
# Read in data:

# Use numpy loadtext function to unpack data from ascii file
lon, u, v, t = np.loadtxt(gdf.get("ascii_files/xy.asc"), unpack=True)

# Do some unit conversions
lon = lon * 360/128
t = (t - 273.15) * 9/5 * 32

################################################################################
# Plot:
fig, ax1 = plt.subplots(figsize=(10,10))

gvutil.add_major_minor_ticks(ax1,
                             y_minor_per_major=5,
                             labelsize=14)
gvutil.set_axes_limits_and_ticks(ax1,
                                 ylim=(-3500, -2900))
ax1.plot(lon, t, linewidth=0.5, c='red')


ax2 = ax1.twinx()
gvutil.add_major_minor_ticks(ax2,
                             y_minor_per_major=5,
                             labelsize=14)
gvutil.set_axes_limits_and_ticks(ax2,
                                 ylim=(10, 60))
ax2.tick_params('both',
                which='both',
                bottom=False,
                top=False,
                left=False)
ax2.plot(lon, u, linewidth=0.5, c='green')


ax3 = ax1.twinx()
ax3.spines['right'].set_position(('axes', 1.1))
gvutil.add_major_minor_ticks(ax3,
                             x_minor_per_major=5, 
                             y_minor_per_major=4,
                             labelsize=14)
gvutil.set_axes_limits_and_ticks(ax3,
                                 xlim=(0, 360),
                                 ylim=(-16, 12),
                                 xticks=[0, 100, 200, 300],
                                 yticks=np.arange(-16, 13, 4))
ax3.tick_params('both',
                which='both',
                bottom=False,
                top=False,
                left=False)
ax3.plot(lon, v, linewidth=0.5, c='blue')

plt.show()
