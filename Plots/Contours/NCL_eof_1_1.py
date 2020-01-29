"""
NCL_eof_1_1.py
===============
Calculate EOFs of the Sea Level Pressure over the North Atlantic.

Concepts illustrated:
  - Calculating EOFs
  - Drawing a time series plot
  - Using coordinate subscripting to read a specified geographical region
  - Rearranging longitude data to span -180 to 180
  - Calculating symmetric contour intervals
  - Drawing filled bars above and below a given reference line
  - Drawing subtitles at the top of a plot
  - Reordering an array

Reproduces the NCL script found here:
https://www.ncl.ucar.edu/Applications/Scripts/eof_1.ncl
"""

###############################################################################
# Import the necessary python libraries
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.viz as gcv

###############################################################################
# Open the file for reading and print a content summary.
ds = xr.open_dataset('../../data/netcdf_files/slp.mon.mean.nc')

print(ds)


###############################################################################
# Flip longitude coordinates.
print(f'Before flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')

ds["lon"] = ((ds["lon"] + 180) % 360) - 180

# Sort longitudes, so that subset operations end up being simpler.
ds["lon"] = np.sort(ds["lon"])

print(f'After flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')


###############################################################################
# Reverse latitude ordering.

# Array indexing syntax is usually [start:end:stride], but here we leave off
# start and end to indicate the full array.
ds["lat"] = ds["lat"][::-1]

print('After reversing latitude values, ds["lat"] is:')

print(ds["lat"])

###############################################################################
# Subset the data.

# Get the surface level pressure variable.
slp = ds.slp

# Limit data to the years 1979-2003, and the Northern Atlantic region.
slp = slp.sel(time=slice('1979-01-1', '2003-12-01'), lat=slice(25, 80), lon=slice(-70, 40))
print(slp)
