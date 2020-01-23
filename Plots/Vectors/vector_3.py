"""
vector_3
========

Plot U & V vectors globally

https://www.ncl.ucar.edu/Applications/Scripts/vector_3.ncl
"""

###############################################################################
# Import necessary packages
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs

###############################################################################
# Read in data from netCDF file
file_in = xr.open_dataset('../../data/netcdf_files/uv300.nc')

###############################################################################
# Extract required variables from files
lat = file_in['lat']
lon = file_in['lon']

u = file_in['U'].isel(time=1)
v = file_in['V'].isel(time=1)

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
# Make the plot

# Set up figure and axes
fig, ax = plt.subplots(figsize=(10,7))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Zonal Wind\n')
nclize_axis(ax)
add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xticks(range(-180, 181, 30))
plt.yticks(range(-90, 91, 30))

# Draw vector plot
# Notes
# 1. We plot every third vector in each direction, which is not as nice as vcMinDistanceF in NCL
# 2. There is no matplotlib equivalent to "CurlyVector"
Q = plt.quiver(lon[::3], lat[1::3], u.data[1::3, ::3], v.data[1::3, ::3], color='black',
               scale=(10/0.045), zorder=1, pivot="middle", width=0.00075, headwidth=15)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 0.875, 0.8, 10, r'10 $m/s$', labelpos='N',
                  coordinates='figure', color='black', zorder=2)

# Turn on continent shading
feature = cartopy.feature.NaturalEarthFeature(name='coastline',
                                              category='physical',
                                              scale='50m',
                                              edgecolor='lightgray',
                                              facecolor='lightgray',
                                              zorder=0)
ax.add_feature(feature)

# Generate plot!
plt.show()
