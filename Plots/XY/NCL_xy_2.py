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

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset("../../data/netcdf_files/uv300.nc")
U = ds.U

###############################################################################
fig = plt.gcf()
ax = plt.gca()

# Plot data
U.isel(time=0).sel(lon=82, method='nearest').plot(x="lat", marker='', color='#C0C2EA', linewidth=1.1)
U.isel(time=0).sel(lon=-69, method='nearest').plot(x="lat", marker='', color='#E28D90', linewidth=1.1, linestyle='--', dashes=[6.5, 3.7])

###############################################################################
# Adjust figure size and plot parameters to get identical to original NCL plot
fig.set_size_inches((7, 6.5))

# Hard-code tic values.
ax.set_xticks(np.linspace(-90, 90, 7))
ax.set_yticks(np.linspace(-20, 50, 8))

# Modify x-axis tick labels to be shown as North (N) - South (S) latitudinal.
# Cartopy LatitudeFormatter could be used here, but it is not necessary (it would cost projection loading) since this is
# only a XY-plot. Therefore, just hard-code for this case:
ax.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'])

# Tweak minor tic marks. Set spacing so we get nice round values.
ax.tick_params(labelsize=16)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
ax.tick_params('both', length=10, width=0.5, which='major', top=True, right=True)
ax.tick_params('both', length=5, width=0.25, which='minor', top=True, right=True)

# Set title, axis labels and limits, etc.
ax.set_title("Two Curve XY Plot", fontsize=20, y=1.04)
ax.set_xlim((-90,90))
ax.set_ylim((-20,50))
ax.set_xlabel("")
ax.set_ylabel("Zonal Wind", fontsize=18)

###############################################################################
# Show the plot
plt.show(block=True)

