"""
NCL_trans_1.py
==============
Calculate and plot a transect

This script illustrates the following concepts:
  - 

See following URLs to see the reproduced NCL plot & script:
  - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/trans_1.ncl
  - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/trans_1_1_lg.png

"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
from pyproj import Geod
from metpy.interpolate import cross_section
import cmaps
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LatitudeFormatter, LongitudeFormatter

import geocat.datafiles as gdf
import geocat.viz as gv
from geocat.comp import interp_multidim

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

# Add attrs for CF compliance to work with metpy package
ds.time_bound.attrs['units'] = 'days since 0000-01-01 00:00:00'
ds.time_bound.attrs['calendar'] = 'noleap'
ds.time.attrs['calendar'] = 'noleap'

ds = xr.decode_cf(ds)

# format for metpy
ds = ds.metpy.assign_crs(
    grid_mapping_name='latitude_longitude',
    earth_radius=6371229.0
).rename({"lat_t": "lat", "lon_t": "lon"})


# Pull out temperature
t = ds.T[0,:,:,:]
##############################################################################
# Calculate the great circle transect

leftlat = -60
rightlat = -30

leftlon = -60
rightlon = 20

npts = 100

# geodesic = Geod(ellps="sphere")
# newpts = geodesic.npts(leftlat, leftlon, rightlat, rightlon, npts=npts)
# _, _, gcdist = geodesic.inv(leftlat, leftlon, rightlat, rightlon)
# gcdist = gcdist/1000    # convert to km

##############################################################################
# Interpolate to great circle

transect = cross_section(t, (leftlat, leftlon), (rightlat, rightlon), steps=npts)
##############################################################################
# Plot

cmap = 'viridis'
#cmap = cmaps.BlAqGrYeOrReVi200

fig, ax = plt.subplots(1, 1)
p = ax.contourf(transect, cmap=cmap, levels=21)
# ax.contourf(transect.lat, transect.z_t, transect, cmap=cmap, levels=21)
# ax.set_yscale('log')
ax.invert_yaxis()
ax.set_xlim
fig.colorbar(p)
plt.xlim(0, 90)

# Plot transect locations
projection = ccrs.PlateCarree()
fig1 = plt.figure()

ax1 = fig1.add_subplot(1, 1, 1, projection=projection)
ax1.set_global()

# Draw land
ax1.add_feature(cfeature.LAND, color='lightgrey')

# Add line
ax1.plot([leftlon, rightlon], [leftlat, rightlat], 
            transform=projection, color='red', linewidth=1)

# Formatting
# Use geocat.viz.util convenience function to set axes tick values
gv.set_axes_limits_and_ticks(
    ax1, xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7)
)
gv.add_lat_lon_ticklabels(ax1)

# Remove the degree symbol from tick labels
ax1.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax1.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

# Add minor ticks
gv.add_major_minor_ticks(ax1, x_minor_per_major=3, y_minor_per_major=4)

# Use geocat.viz.util convenience function to add title
gv.set_titles_and_labels(ax1, maintitle="Transect Location")

# Show plots
plt.tight_layout()
plt.show()