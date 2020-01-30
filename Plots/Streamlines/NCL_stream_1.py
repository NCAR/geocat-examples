"""
NCL_stream_1.py
===============
Basic streamlines drawing

Concepts illustrated:
   - Drawing a black-and-white streamline plot over a map

Replicates the NCL script: https://www.ncl.ucar.edu/Applications/Scripts/stream_1.ncl
"""

################################################################################
#
# import modules
#
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import geocat.viz as gcv
import geocat.datafiles


################################################################################
#
# open data file and extract variables. We extract a 2D horzontal slice from
# the first time step of the 3D U and V variables at the at the bottom level.
#
ds = xr.open_dataset(geocat.datafiles.get('netcdf_files/uvt.nc'))

timestep = 0
level = 0
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



#
# Set up tick marks to look like NCL plots, and configure tick labels
#
gcv.util.nclize_axis(ax)
gcv.util.add_lat_lon_ticklabels(ax)

#
# Hard-code tic values. This assumes data are global
#
ax.set_xticks(np.linspace(-180, 180, 13), crs=projection)
ax.set_yticks(np.linspace(-90, 90, 7), crs=projection)


#
# Draw filled polygons for land
#
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black', color='lightgray')

#
# Subtitle for plot. Need to specify a y displacement otherwise title
# overlaps tick marks
#
ypos = 1.04
ax.set_title(U.long_name + ' (' + U.units+')', fontsize=18, loc='left', y=ypos)


#
# Use global map
#
ax.set_global()


#
# There is no Xarray streamplot function. So need to call 
# matplotlib.streamplot directly. Not sure why, but can't pass xarray.DataArray
# objects directly: fetch NumPy arrays via 'data' attribute'
#
ax.streamplot(U.lon.data, U.lat.data, U.data, V.data, linewidth=1, density=4, color='black', zorder=1)
plt.show()
