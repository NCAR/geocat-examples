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
import matplotlib.pyplot as plt


###############################################################################
# 
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/atmos.nc', decode_times=False)
v = ds.V.isel(time=0, lev = 3)

###############################################################################
# 
# create plot
fig = plt.figure(figsize=(10,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(linewidths=0.5)

xticks = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
xlabels = ['180', '150W', '120W', '90W', '60W', '30W', '0', '30E', '60E', '90E', '120E', '150E', '180']
yticks = [-90, -60, -30, 0, 30, 60, 90]
ylabels = ['90S', '60S', '30S', '0', '30N', '60N', '90N']
plt.xticks(xticks, xlabels)
plt.yticks(yticks, ylabels)
plt.minorticks_on()
plt.tick_params(which='both',right=True, top=True)

v.plot.contourf(levels = 14, cmap = 'tab20b', cbar_kwargs={"label":'', "shrink":0.4})
v.plot.contour(levels = 14, linewidths=0.5, cmap='k')

plt.title('meridional wind component        m/s')
plt.xlabel('')
plt.ylabel('')

plt.show();