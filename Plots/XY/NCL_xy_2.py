"""
NCL_xy_2.py
===============
This script illustrates the following concepts:
   - Drawing an XY plot with multiple curves
   - Changing the line color for multiple curves in an XY plot
   - Changing the line thickness for multiple curves in an XY plot
   - Drawing XY plot curves with both lines and markers
   - Changing the default markers in an XY plot
   - Making all curves in an XY plot solid.
See https://www.ncl.ucar.edu/Applications/xy.shtml for further information.
"""

###############################################################################
# Import packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset("../../data/netcdf_files/uv300.nc")
u = ds.U[:]

###############################################################################
# Generate plot data from netCDF data
# xx = u.values[0,:,82]
xx = u[0,:,:].sel(lon=[82], method='nearest')
# yy = u.values[0,:,-69]
yy = u[0,:,:].sel(lon=[-69], method='nearest')
lat = u['lat'].values

###############################################################################
# Multiple line plot
fig = plt.figure()
ax = plt.axes()

# Hard-code tic values. This assumes data are global
ax.set_xticks(np.linspace(-90, 90, 7))
ax.set_yticks(np.linspace(-20, 50, 8))

# Hard-code x-axis tick labels
ax.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'])

# Tweak minor tic marks. Set spacing so we get nice round values (10 degrees). Again, assumes global data
ax.tick_params(labelsize=16)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
ax.tick_params('both', length=10, width=0.5, which='major')
ax.tick_params('both', length=5, width=0.25, which='minor')

# Plot data
plt.plot( lat, xx, marker='', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=1)
plt.plot( lat, yy, marker='', color='red', linewidth=1, linestyle='dashed', label="toto")
plt.title("Two Curve XY Plot")
ax.set_xlim((-90,90))
ax.set_ylim((-20,50))
plt.ylabel("Zonal Wind")

plt.show(block=True)

