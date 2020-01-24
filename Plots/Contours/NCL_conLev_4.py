"""
NCL_conLev_4.py
===============
This script illustrates the following concepts:
   - Explicitly setting contour levels
   - Explicitly setting the fill colors for contours
   - Reordering an array
   - Removing the mean
   - Drawing color-filled contours over a cylindrical equidistant map
   - Turning off contour line labels
   - Turning off contour lines
   - Turning off map fill
   - Turning on map outlines
See https://www.ncl.ucar.edu/Applications/Scripts/conLev_4.ncl for further information.
"""

###############################################################################
# Import packages
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.util as cutil
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from util.make_byr_cmap import make_byr_cmap

import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import matplotlib.cm as cm

###############################################################################
# Define a function that handles NCL's dim_rmvmean_n_Wrap's work
def NCL_dim_rmvmean_n_Wrap(arr, dim):
    arr_mean = arr.mean('time')
    print(arr.shape)
    print(arr_mean.shape)
    return arr_mean

###############################################################################
# Define a utility function that handles the no-shown-data artifact of 0 and 360-degree longitudes
def xr_add_cyclic(da, coord):
    cyclic_data, cyclic_coord = cutil.add_cyclic_point(da.values, coord=da[coord])

    coords = da.coords.to_dataset()
    coords[coord] = cyclic_coord
    return xr.DataArray(cyclic_data, dims=da.dims, coords=coords.coords)

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset("../../data/netcdf_files/b003_TS_200-299.nc", decode_times=False)
x = ds.TS

# Apply mean reduction from coordinates as performed in NCL's dim_rmvmean_n_Wrap(x,0)
# Apply this only to x.isel(time=0) because NCL plot plots only for time=0
newx = x.mean('time')
newx = x.isel(time=0) - newx

# Resolve the no-shown-data artifact of 0 and 360-degree longitudes
newx = xr_add_cyclic(newx, "lon")

###############################################################################
# Plot
# First get axes for a projection of preference
fig = plt.figure()
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Use global map, which leaves a gap at end of plot. This data set isn't truly global.
ax.set_global()
ax.coastlines(linewidth=0.5, resolution="110m")

# Import an NCL colormap
newcmp = make_byr_cmap()

# Plot filled contours
p = newx.plot.contourf(ax=ax, vmin=-1, vmax=10, levels=[-12,-10,-8,-6,-4,-2,-1,1,2,4,6,8,10,12], cmap=newcmp, add_colorbar=False, transform=projection, add_labels=False)

###############################################################################
# Adjust figure size and plot parameters to get identical to original NCL plot
fig.set_size_inches((15, 9))

# Hard-code tic values. This assumes data are global
ax.set_xticks(np.linspace(-180, 180, 13), crs=projection)
ax.set_yticks(np.linspace(-90, 90, 7), crs=projection)

# Use cartopy's lat and lon formatter to get tic values displayed in degrees
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# Tweak minor tic marks. Set spacing so we get nice round values (10 degrees). Again, assumes global data
ax.tick_params(labelsize=16)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.tick_params('both', length=20, width=2, which='major', top=True, right=True)
ax.tick_params('both', length=10, width=1, which='minor', top=True, right=True)

# Add horizontal colorbar
cbar = plt.colorbar(p, orientation='horizontal', shrink=0.5)
cbar.ax.tick_params(labelsize=16)
cbar.set_ticks([-12,-10,-8,-6,-4,-2,-1,1,2,4,6,8,10,12])

# Add titles to left and right of the plot axis.
ax.set_title('Anomalies: Surface Temperature', y=1.04, fontsize=18, loc='left')
ax.set_title('K', y=1.04, fontsize=18, loc='right')

###############################################################################
# Show the plot
plt.show(block=True)