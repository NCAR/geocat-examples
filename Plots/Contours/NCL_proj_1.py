"""
proj_1_lg
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
t = ds.TS.isel(time=0)

#wrap data around meridian
lon_idx = t.dims.index('lon')
wrap_data, wrap_lon = add_cyclic_point(t.values, coord=t.lon, axis=lon_idx)
wrap_t = xr.DataArray(wrap_data, coords=[t.lat, wrap_lon], dims=['lat', 'lon'], attrs = t.attrs)

###############################################################################
# 
# create plot
fig = plt.figure(figsize=(10,10))

# use Cartopy to specify projection and add coastlines and gridlines
ax = plt.axes(projection=ccrs.Mollweide())
ax.coastlines(linewidths=0.5)

gl = ax.gridlines(crs=ccrs.PlateCarree(),
                  linewidth=1, color='k', alpha=0.5)

# use a filled contour and an additional contour to add black boundary between levels.
wrap_t.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), 
                    levels = 11, cmap = 'gist_rainbow_r', 
                    cbar_kwargs={"orientation": "horizontal", "label":'', "shrink":0.9})
wrap_t.plot.contour(ax=ax, transform=ccrs.PlateCarree(), 
                    levels = 11, linewidths=0.5, cmap='k')

# add title and suptitle
plt.suptitle('Example of a Mollweide Projection', y = .8, fontsize=18)
plt.title('Surface Temperature                       K', fontsize=14)

plt.show();