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
# Flip and sort longitude coordinates, to facilitate data subsetting.

print(f'Before flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')

ds["lon"] = ((ds["lon"] + 180) % 360) - 180

# Sort longitudes, so that subset operations end up being simpler.
ds = ds.sortby("lon")

print(f'After flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')


###############################################################################
# Place latitudes in increasing order to facilitate data subsetting.

# Array indexing syntax is usually [start:end:stride], but here we leave off
# start and end to indicate the full array.
ds = ds.sortby("lat", ascending=True)

print('After reversing latitude values, ds["lat"] is:')

print(ds["lat"])

###############################################################################
# Subset the data.

# Get the surface level pressure variable.
slp = ds.slp

# Limit data to the years 1979-2003, and the Northern Atlantic region.
slp = slp.sel(time=slice('1979-01-1', '2003-12-01'), lat=slice(25, 80), lon=slice(-70, 40))
print(slp)

###############################################################################
# Define a utility function for computing seasonal means.

def month_to_season(xMon, season):
    """ This function takes an xarray dataset containing monthly data spanning years and
        returns a dataset with one value per year, for a specified three-month season.

        Time stamps are centered on the season, e.g. seasons='DJF' returns January timestamps.
    """
    seasons_pd = {'DJF': ('QS-DEC', 1), 'JFM': ('QS-JAN',  2), 'FMA': ('QS-FEB',  3), 'MAM': ('QS-MAR',  4),
                  'AMJ': ('QS-APR', 5), 'MJJ': ('QS-MAY',  6), 'JJA': ('QS-JUN',  7), 'JAS': ('QS-JUL',  8),
                  'ASO': ('QS-AUG', 9), 'SON': ('QS-SEP', 10), 'OND': ('QS-OCT', 11), 'NDJ': ('QS-NOV', 12)}
    try:
        (season_pd, month_sel) = seasons_pd[season]
    except KeyError:
        raise ValueError("contributed: month_to_season: bad season: SEASON = " + season)

    # Compute the three-month means, moving time labels ahead to the middle month.
    month_offset = 'MS'
    xSeasons = xMon.resample(time=season_pd, loffset=month_offset).mean()

    # Filter just the desired season
    xSea = xSeasons.sel(time=xSeasons.time.dt.month.isin(month_sel))
    return xSea

