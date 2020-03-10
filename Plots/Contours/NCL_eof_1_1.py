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
import xarray as xr
import geocat.datafiles
from math import atan
import numpy as np
from numpy import cos, sqrt    # numpy's cos(), sqrt() accept array arguments.

from geocat.comp import eofunc, eofunc_ts

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import geocat.viz as gcv
import cartopy.crs as ccrs


###############################################################################
# User defined parameters that specify region of the globe, time span, etc.
latS = 25.
latN = 80.
lonL = -70.
lonR = 40.

yearStart = 1979
yearEnd = 2003

neof = 3   # number of EOFs
optETS = False


###############################################################################
# Open the file for reading and print a content summary.

ds = xr.open_dataset(geocat.datafiles.get('netcdf_files/slp.mon.mean.nc'))

print('\nds.slp.attrs:\n')
print(ds.slp.attrs)


###############################################################################
# Flip and sort longitude coordinates, to facilitate data subsetting.

print(f'Before flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')

ds["lon"] = ((ds["lon"] + 180) % 360) - 180

# Sort longitudes, so that subset operations end up being simpler.
ds = ds.sortby("lon")

print(f'After flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].')


###############################################################################
# Place latitudes in increasing order to facilitate data subsetting.

ds = ds.sortby("lat", ascending=True)

print('After sorting latitude values, ds["lat"] is:')

print(ds["lat"])

###############################################################################
# Limit data to the specified years.

startDate = f'{yearStart}-01-01'
endDate = f'{yearEnd}-12-01'

ds = ds.sel(time=slice(startDate, endDate))
print('\n\nds:\n\n')
print(ds)

###############################################################################
# Define a utility function for computing seasonal means.

def month_to_season(xMon, season, startDate, endDate):
    """ This function takes an xarray dataset containing monthly data spanning years and
        returns a dataset with one sample per year, for a specified three-month season.

        Time stamps are centered on the season, e.g. seasons='DJF' returns January timestamps.
    """
    startDate = xMon.time[0]
    endDate = xMon.time[-1]
    seasons_pd = {'DJF': ('QS-DEC', 1), 'JFM': ('QS-JAN',  2), 'FMA': ('QS-FEB',  3), 'MAM': ('QS-MAR',  4),
                  'AMJ': ('QS-APR', 5), 'MJJ': ('QS-MAY',  6), 'JJA': ('QS-JUN',  7), 'JAS': ('QS-JUL',  8),
                  'ASO': ('QS-AUG', 9), 'SON': ('QS-SEP', 10), 'OND': ('QS-OCT', 11), 'NDJ': ('QS-NOV', 12)}
    try:
        (season_pd, season_sel) = seasons_pd[season]
    except KeyError:
        raise ValueError("contributed: month_to_season: bad season: SEASON = " + season)

    # Compute the three-month means, moving time labels ahead to the middle month.
    month_offset = 'MS'
    xSeasons = xMon.resample(time=season_pd, loffset=month_offset).mean()

    # Filter just the desired season, and trim to the desired time range.
    xSea = xSeasons.sel(time=xSeasons.time.dt.month.isin(season_sel))
    xSea = xSea.sel(time=slice(startDate, endDate))
    return xSea

###############################################################################
# Compute desired global seasonal mean using month_to_season()

# Choose the winter season (December-January-February)
season = "DJF"
SLP = month_to_season(ds, season, startDate, endDate)
print('\n\nSLP:\n\n')
print(SLP)

# Diagnostic plot: show slice of SLP
sliceSLP = SLP.sel(lat=slice(latS, latN), lon=slice(lonL, lonR))

print('\n\nsliceSLP:\n\n')
print(sliceSLP)

###############################################################################
# Create weights: sqrt(cos(lat))   [or sqrt(gw) ]

deg2rad = 4. * atan(1.) / 180.
clat = SLP['lat']
clat = sqrt(cos(deg2rad * clat))
print(clat)

###############################################################################
# Multiply SLP by weights.
#
# Xarray uses the supplied coordinate information to apply latitude-based
# weights to all longitudes and timesteps automatically.

wSLP = SLP
wSLP['slp'] = clat * SLP['slp']

# For now, metadata for slp must be copied over explicitly; it is not preserved by binary operators like multiplication.
wSLP['slp'].attrs = ds['slp'].attrs
wSLP['slp'].attrs['long_name'] = 'Wgt: ' + wSLP['slp'].attrs['long_name']

###############################################################################
# Subset data to the North Atlantic region.

xw = wSLP.sel(lat=slice(latS, latN), lon=slice(lonL, lonR))

print('\n\nxw:\n\n')
print(xw.slp)

###############################################################################
# Compute the EOFs.

eof = eofunc(xw["slp"], neof, time_dim=1, meta=True)

print('\n\neof:\n\n')
print(eof)

eof_ts = eofunc_ts(xw["slp"], eof, time_dim=1, meta=True)

print('\n\neof_ts:\n\n')
print(eof_ts)


###############################################################################
# Normalize time series: Sum spatial weights over the area used.
nLon = len(xw['lon'])
weightTotal = clat.sum() * nLon
eof_ts = eof_ts / weightTotal

print('\n\neof_ts normalized:\n\n')
print(eof_ts)

###############################################################################
# Create a utility function for a basic plot.

def make_base_plot(ax, dataset):

    map_extent = [lonL, lonR, latS, latN]

    # Add tick marks to match NCL conventions.
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(AutoMinorLocator(n=3))
    ax.yaxis.set_minor_locator(AutoMinorLocator(n=4))
    ax.set_extent(map_extent, crs=ccrs.PlateCarree())
    ax.set_xticks([-60, -30, 0, 30])
    ax.set_yticks([40, 60, 80])
    ax.tick_params("both", length=5, width=1.0, which="major", bottom=True, left=True, top=True, right=True, labelsize=8)
    ax.tick_params("both", length=3.5, width=0.5, which="minor", bottom=True, left=True, top=True, right=True, labelsize=8)

    lat = dataset['lat']
    lon = dataset['lon']
    values = dataset.data

    cmap = plt.get_cmap('bwr')

    # Specify levels
    v = np.linspace(-0.08, 0.08, 9, endpoint=True)

    cplot = ax.contourf(lon, lat, values, levels=v, cmap=cmap, extend="both")
    #ax.clabel(cplot, fontsize="small", fmt="%0.2f", colors="k", inline=True)

    ax.coastlines()
    gcv.util.add_lat_lon_ticklabels(ax)
    return cplot, ax


fig, axs = plt.subplots(neof, 1,
                        constrained_layout=True,  # "magic"
                        subplot_kw={"projection": ccrs.PlateCarree()},
                        figsize=(7, 8))

for i in range(neof):

    eof_single = eof.sel(evn=i)

    cplot, axs[i] = make_base_plot(axs[i], eof_single)

    axs[i].set_title(f'EOF {i+1}', y=1.02, loc='left', fontsize=10)
    pct = eof.pcvar[i]
    axs[i].set_title(f'{pct:.1f}%', y=1.02, loc='right', fontsize=10)

cbar = fig.colorbar(cplot, ax=axs, orientation='horizontal', shrink=0.6)

fig.suptitle(f'SLP: DJF: {yearStart}-{yearEnd}')

plt.savefig('test.png')

plt.show()





###############################################################################
# Produce bar plot.


print("Done.")