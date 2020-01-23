"""
NCL_stream_1.py
===============
Basic streamlines drawing

Drawing a black-and-white streamline plot over a map
"""

################################################################################
#
# Convenience function for setting up tickmarks for global data
#
def nclize_axis(ax):
  """
  Utility function to make plots look like NCL plots
  """
  import matplotlib.ticker as tic

  #ax.tick_params(labelsize="small")
  ax.tick_params(labelsize=16)
  ax.minorticks_on()
  ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
  ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))

  # length and width are in points and may need to change depending on 
  # figure size etc.
  #
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

################################################################################
#
# import modules
#
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.geoaxes import GeoAxes


################################################################################
#
# open data file and extract variables. We extract a 2D horzontal slice from
# the first time step of the 3D U and V variables at the at the bottom level.
#
timestep = 0
level = 0
ds = xr.open_dataset('../../data/netcdf_files/uvt.nc')
U = ds.U[timestep,level,:,:]
V = ds.V[timestep,level,:,:]


################################################################################
#
#
plt.rcParams['figure.figsize'] = [16, 8]
fig = plt.figure()
fig.suptitle('Example of a streamline plot', fontsize=22, fontweight='bold')

projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)


################################################################################
#
# Hard-code tic values. This assumes data are global
#
ax.set_xticks(np.linspace(-180, 180, 13), crs=projection)
ax.set_yticks(np.linspace(-90, 90, 7), crs=projection)

#
# Use cartopy's lat and lon formatter to get tic values displayed in degrees
#
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)


#
# Set up tick marks to look like NCL plots
#
nclize_axis(ax)

#
# Draw filled polygons for land
#
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black', color='lightgray')

#
# Subtitle for plot. Need to specify a y displacement otherwise title
# overlaps tick marks
#
ydisplacement = 1.04
ax.set_title(U.long_name + ' (' + U.units+')', fontsize=18, loc='left', y=ydisplacement)


#
# Use global map
#
ax.set_global()
ax.coastlines()


################################################################################
#
# There is no Xarray streamplot function. So need to call 
# matplotlib.streamplot directly. Not sure why, but can't pass xarray.DataArray
# objects directly: fetch NumPy arrays via 'data' attribute'
#
ax.streamplot(U.lon.data, U.lat.data, U.data, V.data, linewidth=1, density=4, color='black')
plt.show()
