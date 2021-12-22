"""
calendar_average_example.py
===========================
This script illustrates the following concepts:
    - Usage of geocat-comp's `calendar_average <https://geocat-comp.readthedocs.io/en/latest/user_api/generated/geocat.comp.climatologies.calendar_average.html?highlight=CALENDER%20average>`_ function.
    - Usage of geocat-datafiles for accessing NetCDF files
    - Creating a figure with stacked subplots

See following GitHub repositories to see further information about the function and how to access
data:
    - For GeoCAT functions: https://github.com/NCAR/geocat-comp
    - For atm.20C.hourly6-1990-1995.nc file: https://github.com/NCAR/geocat-datafiles/tree/main/netcdf_files

Dependencies:
    - cftime
    - geocat.comp
    - geocat.datafiles (Not necessary for figure but used for accessing the data file)
    - geocat.viz
    - matplotlib
    - xarray
"""

###############################################################################
# Import packages

import cftime
import matplotlib.pyplot as plt
import xarray as xr

from geocat.comp import calendar_average
import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

ds = xr.open_dataset(gdf.get('netcdf_files/atm.20C.hourly6-1990-1995-TS.nc'))
ds = ds.isel(member_id=0)  # select one model from the ensemble

temp = ds.TS # surface temperature data

###############################################################################
# Calculate climatologies using `calendar_average`

daily = calendar_average(temp, 'day')
monthly = calendar_average(temp, 'month')
season = calendar_average(temp, 'season')

# Convert datetimes to number of hours since 1990-01-01 00:00:00
# This must be done in order to use the time for the x axis
time_num_raw = cftime.date2num(temp.time, 'hours since 1990-01-01 00:00:00')
time_num_day = cftime.date2num(daily.time, 'hours since 1990-01-01 00:00:00')
time_num_month = cftime.date2num(monthly.time, 'hours since 1990-01-01 00:00:00')
time_num_season = cftime.date2num(season.time, 'hours since 1990-01-01 00:00:00')

# Start and end time for axes limits
tstart = time_num_raw[0]
tend = time_num_raw[-1]

###############################################################################
# Plot:

# Make three subplots with shared axes
fig, ax = plt.subplots(4, 1, figsize=(8, 10),
                       sharex=True, sharey=True, constrained_layout=True)

# Plot data
ax[0].plot(time_num_raw, temp.data)
ax[1].plot(time_num_day, daily.data)
ax[2].plot(time_num_month, monthly.data)
ax[3].plot(time_num_season, season.data)

# Use geocat.viz.util convenience function to set axes parameters without
# calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(ax[0],
                                 xlim=(tstart, tend+1),
                                 xticks=range(tstart, tend+1, 365*24),
                                 xticklabels=range(1990, 1997),
                                 ylim=(297, 304))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax[0],
                             ylabel='Raw Data (6-hourly)',
                             lefttitle=temp.long_name,
                             lefttitlefontsize=14,
                             righttitle=temp.units,
                             righttitlefontsize=14)

gvutil.set_titles_and_labels(ax[1],
                             ylabel='Daily Average')

gvutil.set_titles_and_labels(ax[2],
                             ylabel='Monthly Average')

gvutil.set_titles_and_labels(ax[3],
                             ylabel='Season Average',
                             xlabel=temp.time.long_name)

plt.show()
