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
from math import atan
import numpy as np
from numpy import cos, sqrt    # numpy's cos(), sqrt() accept array arguments.

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
from geocat.comp import eofunc, eofunc_ts
from geocat.viz import cmaps as gvcmaps

import matplotlib.pyplot as plt

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

ds = xr.open_dataset(gdf.get('netcdf_files/slp.mon.mean.nc'))

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

def month_to_season(xMon, season):
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
SLP = month_to_season(ds, season)
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
clat_subset = clat.where((clat.lat >= latS) & (clat.lat <= latN), drop=True)
weightTotal = clat_subset.sum() * nLon
eof_ts = eof_ts / weightTotal

print('\n\neof_ts normalized:\n\n')
print(eof_ts)


###############################################################################
# Define a utility function for creating a contour plot.

def make_contour_plot(ax, dataset):

    map_extent = [lonL, lonR, latS, latN]
    ax.set_extent(map_extent, crs=ccrs.PlateCarree())

    # Use geocat.viz.util convenience function to set axes tick values
    gvutil.set_axes_limits_and_ticks(ax, xlim=None, ylim=None, xticks=[-60, -30, 0, 30], yticks=[40, 60, 80])

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=4, labelsize=10)

    lat = dataset['lat']
    lon = dataset['lon']
    values = dataset.data

    cmap = gvcmaps.BlWhRe

    # Specify contour levels
    v = np.linspace(-0.08, 0.08, 9, endpoint=True)

    # The function contourf() produces fill colors, and contour() calculates contour label locations.
    cplot = ax.contourf(lon, lat, values, levels=v, cmap=cmap, extend="both")
    p = ax.contour(lon, lat, values, levels=v, linewidths=0.0)
    ax.clabel(p, fontsize=8, fmt="%0.2f", colors="k")

    ax.coastlines(linewidth=0.5)
    gvutil.add_lat_lon_ticklabels(ax)
    return cplot, ax


###############################################################################
# Draw a contour plot for each EOF.

fig, axs = plt.subplots(neof, 1,
                        constrained_layout=True,  # "magic"
                        subplot_kw={"projection": ccrs.PlateCarree()},
                        figsize=(6, 9))

for i in range(neof):

    eof_single = eof.sel(evn=i)

    cplot, axs[i] = make_contour_plot(axs[i], eof_single)

    # Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
    pct = eof.pcvar[i]
    gvutil.set_titles_and_labels(axs[i], maintitle=None, maintitlefontsize=18, lefttitle=f'EOF {i + 1}',
                                 lefttitlefontsize=10, righttitle=f'{pct:.1f}%', righttitlefontsize=10, xlabel=None,
                                 ylabel=None, labelfontsize=16)


cbar = fig.colorbar(cplot, ax=axs, orientation='horizontal', shrink=0.6)
cbar.ax.tick_params(labelsize=8)

fig.suptitle(f'SLP: DJF: {yearStart}-{yearEnd}')

plt.savefig('test.png')

plt.show()


###############################################################################
# Define a utility function for creating a bar plot.

def make_bar_plot(ax, dataset):

    years = list(dataset.time.dt.year)
    values = list(dataset.values)
    colors = ['blue' if val < 0 else 'red' for val in values]

    ax.bar(years, values, color=colors, edgecolor='k')
    ax.set_ylabel('Pa')

    # Add tick marks to match NCL conventions.
    gvutil.add_major_minor_ticks(ax, x_minor_per_major=4, y_minor_per_major=5, labelsize=8)

    return ax


###############################################################################
# Produce a bar plot for each EOF.

fig, axs = plt.subplots(neof, 1,
                        constrained_layout=True,  # "magic"
                        figsize=(6, 9))
for i in range(neof):

    eof_single = eof_ts.sel(neval=i)

    axs[i] = make_bar_plot(axs[i], eof_single)
    pct = eof.pcvar[i]
    gvutil.set_titles_and_labels(axs[i], maintitle=None, maintitlefontsize=18, lefttitle=f'EOF {i + 1}',
                                 lefttitlefontsize=10, righttitle=f'{pct:.1f}%', righttitlefontsize=10, xlabel=None,
                                 ylabel=None, labelfontsize=16)

fig.suptitle(f'SLP: DJF: {yearStart}-{yearEnd}')

plt.show()

