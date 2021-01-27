"""
NCL_eof_1_1.py
===============
Calculate EOFs of the Sea Level Pressure over the North Atlantic.

This script illustrates the following concepts:
  - Calculating EOFs
  - Drawing a time series plot
  - Using coordinate subscripting to read a specified geographical region
  - Rearranging longitude data to span -180 to 180
  - Calculating symmetric contour intervals
  - Drawing filled bars above and below a given reference line
  - Drawing subtitles at the top of a plot
  - Reordering an array

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/eof_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/eof_1_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/eof_1_2_lg.png

Note (1):
    So-called original NCL plot "eof_1_2_lg.png" given in the above URL is likely not identical to what the given NCL original script generates. When the given NCL script is run, it generates a plot with identical data to that is plotted by this Python script.

Note (2):
    This script includes many optional diagnostic print statements to provide information about data slicing. To activate such print statements, the parameter "debug" should be set to True.
"""

###############################################################################
# Import packages:
import xarray as xr
import numpy as np

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
from geocat.viz import cmaps as gvcmaps
from geocat.comp import eofunc, eofunc_ts

import matplotlib.pyplot as plt

import cartopy.crs as ccrs

###############################################################################
# User defined parameters and a convenience function:

# In order to specify region of the globe, time span, etc.
latS = 25.
latN = 80.
lonL = -70.
lonR = 40.

yearStart = 1979
yearEnd = 2003

neof = 3  # number of EOFs

# Set to True to activate diagnostic print statements throughout the code
debug = False


# Convenience function to run diagnostic print statements when "debug" is set to True.
def print_debug(message):
    if debug:
        print(message)


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/slp.mon.mean.nc'))

# Print a content summary
print_debug('\n\nds.slp.attrs:\n')
print_debug(ds.slp.attrs)

###############################################################################
# Flip and sort longitude coordinates:

# To facilitate data subsetting

print_debug(
    f'\n\nBefore flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].'
)

ds["lon"] = ((ds["lon"] + 180) % 360) - 180

# Sort longitudes, so that subset operations end up being simpler.
ds = ds.sortby("lon")

print_debug(
    f'\n\nAfter flip, longitude range is [{ds["lon"].min().data}, {ds["lon"].max().data}].'
)

###############################################################################
# Place latitudes in increasing order:

# To facilitate data subsetting

ds = ds.sortby("lat", ascending=True)

print_debug('\n\nAfter sorting latitude values, ds["lat"] is:')
print_debug(ds["lat"])

###############################################################################
# Limit data to the specified years:

startDate = f'{yearStart}-01-01'
endDate = f'{yearEnd}-12-01'

ds = ds.sel(time=slice(startDate, endDate))
print_debug('\n\nds:\n\n')
print_debug(ds)

###############################################################################
# Utility function:


# Define a utility function for computing seasonal means (to mimmic NCL's month_to_season())
def month_to_season(xMon, season):
    """ This function takes an xarray dataset containing monthly data spanning years and
        returns a dataset with one sample per year, for a specified three-month season.

        Time stamps are centered on the season, e.g. seasons='DJF' returns January timestamps.

        If a calculated season's timestamp falls outside the original range of monthly values, then the calculated mean
        is dropped.  For example, if the monthly data's time range is [Jan-2000, Dec-2003] and the season is "DJF", the
        seasonal mean computed from the single month of Dec-2003 is dropped.
    """
    startDate = xMon.time[0]
    endDate = xMon.time[-1]
    seasons_pd = {
        'DJF': ('QS-DEC', 1),
        'JFM': ('QS-JAN', 2),
        'FMA': ('QS-FEB', 3),
        'MAM': ('QS-MAR', 4),
        'AMJ': ('QS-APR', 5),
        'MJJ': ('QS-MAY', 6),
        'JJA': ('QS-JUN', 7),
        'JAS': ('QS-JUL', 8),
        'ASO': ('QS-AUG', 9),
        'SON': ('QS-SEP', 10),
        'OND': ('QS-OCT', 11),
        'NDJ': ('QS-NOV', 12)
    }
    try:
        (season_pd, season_sel) = seasons_pd[season]
    except KeyError:
        raise ValueError("contributed: month_to_season: bad season: SEASON = " +
                         season)

    # Compute the three-month means, moving time labels ahead to the middle month.
    month_offset = 'MS'
    xSeasons = xMon.resample(time=season_pd, loffset=month_offset).mean()

    # Filter just the desired season, and trim to the desired time range.
    xSea = xSeasons.sel(time=xSeasons.time.dt.month == season_sel)
    xSea = xSea.sel(time=slice(startDate, endDate))
    return xSea


###############################################################################
# Compute desired global seasonal mean using month_to_season()

# Choose the winter season (December-January-February)
season = "DJF"
SLP = month_to_season(ds, season)
print_debug('\n\nSLP:\n\n')
print_debug(SLP)

# Diagnostic plot: show slice of SLP
sliceSLP = SLP.sel(lat=slice(latS, latN), lon=slice(lonL, lonR))

print_debug('\n\nsliceSLP:\n')
print_debug(sliceSLP)

###############################################################################
# Create weights: sqrt(cos(lat))   [or sqrt(gw) ]

deg2rad = np.pi / 180.
clat = SLP['lat'].astype(np.float64)
clat = np.sqrt(np.cos(deg2rad * clat))
print_debug('\n\nclat:\n')
print_debug(clat)

###############################################################################
# Multiply SLP by weights:

# Xarray will apply latitude-based weights to all longitudes and timesteps automatically.
# This is called "broadcasting".

wSLP = SLP
wSLP['slp'] = clat * SLP['slp']

# For now, metadata for slp must be copied over explicitly; it is not preserved by binary operators like multiplication.
wSLP['slp'].attrs = ds['slp'].attrs
wSLP['slp'].attrs['long_name'] = 'Wgt: ' + wSLP['slp'].attrs['long_name']

###############################################################################
# Subset data to the North Atlantic region:

xw = wSLP.sel(lat=slice(latS, latN), lon=slice(lonL, lonR))

print_debug('\n\nxw:\n\n')
print_debug(xw.slp)

###############################################################################
# Compute the EOFs:

eof = eofunc(xw["slp"], neof, time_dim=1, meta=True)

print_debug('\n\neof:\n\n')
print_debug(eof)

eof_ts = eofunc_ts(xw["slp"], eof, time_dim=1, meta=True)

print_debug('\n\neof_ts:\n\n')
print_debug(eof_ts)

###############################################################################
# Normalize time series:

# Sum spatial weights over the area used.
nLon = xw.sizes["lon"]

# Bump the upper value of the slice, so that latitude values equal to latN are included.
clat_subset = clat.sel(lat=slice(latS, latN + 0.01))
weightTotal = clat_subset.sum() * nLon
eof_ts = eof_ts / weightTotal

print_debug('\n\neof_ts normalized:\n\n')
print_debug(eof_ts)

###############################################################################
# Utility function:


# Define a utility function for creating a contour plot.
def make_contour_plot(ax, dataset):
    lat = dataset['lat']
    lon = dataset['lon']
    values = dataset.data

    # Import an NCL colormap
    cmap = gvcmaps.BlWhRe

    # Specify contour levelstamam
    v = np.linspace(-0.08, 0.08, 9, endpoint=True)

    # The function contourf() produces fill colors, and contour() calculates contour label locations.
    cplot = ax.contourf(lon,
                        lat,
                        values,
                        levels=v,
                        cmap=cmap,
                        extend="both",
                        transform=ccrs.PlateCarree())
    p = ax.contour(lon,
                   lat,
                   values,
                   levels=v,
                   linewidths=0.0,
                   transform=ccrs.PlateCarree())

    # Label the contours
    ax.clabel(p, fontsize=8, fmt="%0.2f", colors="black")

    # Add coastlines
    ax.coastlines(linewidth=0.5)

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax,
                                 x_minor_per_major=3,
                                 y_minor_per_major=4,
                                 labelsize=10)

    # Use geocat.viz.util convenience function to set axes tick values
    gvutil.set_axes_limits_and_ticks(ax,
                                     xticks=[-60, -30, 0, 30],
                                     yticks=[40, 60, 80])

    # Use geocat.viz.util convenience function to make plots look like NCL plots, using latitude & longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)

    return cplot, ax


###############################################################################
# Plot (1): Draw a contour plot for each EOF

# Generate figure and axes using Cartopy projection  and set figure size (width, height) in inches
fig, axs = plt.subplots(neof,
                        1,
                        subplot_kw={"projection": ccrs.PlateCarree()},
                        figsize=(6, 10.6))

# Add multiple axes to the figure as contour and contourf plots
for i in range(neof):
    eof_single = eof.sel(evn=i)

    # Create contour plot for the current axes
    cplot, axs[i] = make_contour_plot(axs[i], eof_single)

    # Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
    pct = eof.pcvar[i]
    gvutil.set_titles_and_labels(axs[i],
                                 lefttitle=f'EOF {i + 1}',
                                 lefttitlefontsize=10,
                                 righttitle=f'{pct:.1f}%',
                                 righttitlefontsize=10)

# Adjust subplot spacings and locations
plt.subplots_adjust(bottom=0.07, top=0.95, hspace=0.15)

# Add horizontal colorbar
cbar = plt.colorbar(cplot,
                    ax=axs,
                    orientation='horizontal',
                    shrink=0.9,
                    pad=0.05,
                    fraction=.02)
cbar.ax.tick_params(labelsize=8)

# Set a common title
axs[0].set_title(f'SLP: DJF: {yearStart}-{yearEnd}', fontsize=14, y=1.12)

# Show the plot
plt.show()

###############################################################################
# Utility function:

# Define a utility function for creating a bar plot.


def make_bar_plot(ax, dataset):
    years = list(dataset.time.dt.year)
    values = list(dataset.values)
    colors = ['blue' if val < 0 else 'red' for val in values]

    ax.bar(years,
           values,
           color=colors,
           width=1.0,
           edgecolor='black',
           linewidth=0.5)
    ax.set_ylabel('Pa')

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax,
                                 x_minor_per_major=4,
                                 y_minor_per_major=5,
                                 labelsize=8)

    # Use geocat.viz.util convenience function to set axes tick values
    gvutil.set_axes_limits_and_ticks(ax,
                                     xticks=np.linspace(1980, 2000, 6),
                                     xlim=[1978.5, 2003.5])

    return ax


###############################################################################
# Plot (2): Produce a bar plot for each EOF.

# Generate figure and axes using Cartopy projection and set figure size (width, height) in inches
fig, axs = plt.subplots(neof, 1, constrained_layout=True, figsize=(6, 7.5))

# Add multiple axes to the figure as bar-plots
for i in range(neof):
    eof_single = eof_ts.sel(neval=i)

    axs[i] = make_bar_plot(axs[i], eof_single)
    pct = eof.pcvar[i]
    gvutil.set_titles_and_labels(axs[i],
                                 lefttitle=f'EOF {i + 1}',
                                 lefttitlefontsize=10,
                                 righttitle=f'{pct:.1f}%',
                                 righttitlefontsize=10)

# Set a common title
axs[0].set_title(f'SLP: DJF: {yearStart}-{yearEnd}', fontsize=14, y=1.12)

# Show the plot
plt.show()
