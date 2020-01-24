"""
lb_2
===============
Plots/Contours/Lines
"""

###############################################################################
# 
# import modules
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt



###############################################################################
# 
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/atmos.nc', decode_times=False)
v = ds.V.isel(time=0, lev = 3)

#wrap data around meridian
lon_idx = v.dims.index('lon')
wrap_data, wrap_lon = add_cyclic_point(v.values, coord=v.lon, axis=lon_idx)
wrap_v = xr.DataArray(wrap_data, coords=[v.lat, wrap_lon], dims=['lat', 'lon'], attrs = v.attrs)

###############################################################################
# 
# create plot
fig = plt.figure(figsize=(10,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(linewidths=0.5)

#set y_lim
ax.set_ylim([-90,90])

# here we explicitly specify tick labels to demonstrate how that would be done.
# this allows us to have specific West and East degrees, with 180 and 0 not having such a label.
# consider using the See the add_lat_lon_ticklabels and nclize_axis functions in Cartopy's lat-lon formatter to automate this.
xticks = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
xlabels = ['180', '150W', '120W', '90W', '60W', '30W', '0', '30E', '60E', '90E', '120E', '150E', '180']
yticks = [-90, -60, -30, 0, 30, 60, 90]
ylabels = ['90S', '60S', '30S', '0', '30N', '60N', '90N']
plt.xticks(xticks, xlabels)
plt.yticks(yticks, ylabels)
plt.minorticks_on()
plt.tick_params(which='both',right=True, top=True)

# use a filled contour and an additional contour to add black boundary between levels.
a = wrap_v.plot.contourf(levels = 14, cmap = 'terrain', add_colorbar=False)
wrap_v.plot.contour(levels = 14, linewidths=0.5, cmap='k')

# demonstrate adjusting colorbar tick labels
ticks=[-24,-20,-16,-12,-8,-4,0,4,8,12,16,20, 24]
clabels = ["-90","-70","-50","-30","-10","10","30","50","70","90","110","130","150"]
cbar = fig.colorbar(a, label='', ticks = ticks, shrink=0.4)
cbar.ax.set_yticklabels(clabels)

# add plot title and remove x/y axis labels
plt.title('meridional wind component        m/s')
plt.xlabel('')
plt.ylabel('')

plt.show();