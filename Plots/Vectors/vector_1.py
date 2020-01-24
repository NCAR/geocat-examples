"""
vector_1
========

Plot U & V vector over SST

https://www.ncl.ucar.edu/Applications/Scripts/vector_1.ncl
"""

###############################################################################
# Import necessary packages
import xarray as xr
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cmaps

###############################################################################
# Read in data from netCDF files
sst_in = xr.open_dataset('../../data/netcdf_files/sst8292.nc')
uv_in = xr.open_dataset('../../data/netcdf_files/uvt.nc')

###############################################################################
# Extract required variables from files

# Indices of January 1988 in each file
date_sst = sst_in['date']
date_uv = uv_in['date']
ind_sst = np.where(date_sst == 198801)[0][0]
ind_uv = np.where(date_uv == 198801)[0][0]

# Read in grid information
lat_sst = sst_in['lat']
lon_sst = sst_in['lon']
lat_uv = uv_in['lat']
lon_uv = uv_in['lon']

# Read SST and U, V
sst = sst_in['SST'].isel(time=ind_sst)
u = uv_in['U'].isel(time=ind_uv, lev=0)
v = uv_in['V'].isel(time=ind_uv, lev=0)

###############################################################################
# Define a couple of utility functions
# to make plot look more like NCL style

# Helper function for defining NCL-like ax
def add_lat_lon_ticklabels(ax):
    """
    Nice latitude, longitude tick labels
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(zero_direction_label=False, dateline_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

def nclize_axis(ax):
    """
    Utility function to make plots look like NCL plots
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=1.5,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=5,
        width=0.75,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )

###############################################################################
# The NCL example uses a truncated colormap. Here's a small function that does that
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Utility function that truncates a colormap. Copied from  https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """

    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        name="trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        colors=cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap

###############################################################################
# Make the plot

# Define levels for contour map
levels = np.arange(24,29, 0.1)

# Set up figure
fig, ax = plt.subplots(figsize=(10,7))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Sea Surface Temperature\n')
nclize_axis(ax)
add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xlim([65,95])
plt.ylim([5,25])
plt.xticks(range(70, 95, 10))
plt.yticks(range(5, 27, 5))


# Draw vector plot
Q = plt.quiver(lon_uv, lat_uv, u, v, color='white',
               width=.0025, scale=(4.0/.045), zorder=2)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 0.85, 0.9, 4, r'4 $m/s$', labelpos='N',
                  coordinates='figure', color='black')

# Draw SST contours
plt.cm.register_cmap('BlAqGrYeOrReVi200', truncate_colormap(cmaps.BlAqGrYeOrReVi200, minval=0.08, maxval=0.96, n=len(levels)))
cmap = plt.cm.get_cmap('BlAqGrYeOrReVi200', 50)
cf = ax.contourf(lon_sst, lat_sst, sst, extend='both', levels=levels,
                 cmap=cmap, zorder=0)
cax = plt.axes((0.93, 0.125, 0.02, 0.75))
fig.colorbar(cf, ax=ax, label='$^{\circ}$ C', cax=cax,
             ticks=np.arange(24, 29, 0.3), drawedges=True)

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=1)

# ax.add_feature(feature)
# Generate plot!
plt.show()
