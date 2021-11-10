"""
climatology_example.py
=========================
This script illustrates the following concepts:
    - Usage of geocat-comp's climatology_average and calendar_average functions
    - Usage of geocat-datafiles for accessing NetCDF files

See following GitHub repositories to see further information about the function and how to access
data:
    - For GeoCAT functions: https://github.com/NCAR/geocat-comp
    - For atm.20C.hourly6-1990-1995.nc file: https://github.com/NCAR/geocat-datafiles/tree/main/netcdf_files

Dependencies:
    - cftime
    - geocat.comp
    - geocat.datafiles (Not necessary but for conveniently accessing the data file)
    - geocat.viz
    - matplotlib
    - xarray
"""

###############################################################################
# Import packages

import cftime
import matplotlib.pyplot as plt
import xarray as xr

from geocat.comp import climatology_average, calendar_average
import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

ds = xr.open_dataset('/Users/hcraker/Documents/atm.20C.hourly6-1990-1995-TS.nc')
ds = ds.isel(member_id=0)  # select one model from the ensemble

temp = ds.TS

###############################################################################
# Calculate climatologies using `climatology_average`

daily = climatology_average(temp, 'day')
monthly = climatology_average(temp, 'month')

# Convert datetimes to number of hours since 1990-01-01 00:00:00
# This must be done in order to use the time for the x axis
time_num_raw = cftime.date2num(temp.time, 'hours since 1990-01-01 00:00:00')
time_num_day = cftime.date2num(daily.time, 'hours since 1990-01-01 00:00:00')
time_num_month = cftime.date2num(monthly.time, 'hours since 1990-01-01 00:00:00')

# Start and end time for axes limits
tstart = time_num_raw[0]
tend = time_num_raw[-1]

###############################################################################
# Plot:

# Make three subplots with shared axes
fig, ax = plt.subplots(3, 1, figsize=(8, 10),
                       sharex=True, sharey=True, constrained_layout=True)

# Plot data
ax[0].plot(time_num_raw, temp.data)
ax[1].plot(time_num_day, daily.data)
ax[2].plot(time_num_month, monthly.data)

# Use geocat.viz.util convenience function to set axes parameters without
# calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(ax[0],
                                 xlim=(tstart, tend+1),
                                 ylim=(297, 304))

plt.show()