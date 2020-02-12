"""
proj_1_lg
===============
Plots/Contours/Lines
"""

###############################################################################
# 
# import modules
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt


###############################################################################
# 
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/h_avg_Y0191_D000.00.nc', decode_times=False)
t = ds.T.isel(time=0, z_t=0).sel(lat_t = slice(-60,30), lon_t = slice(30,120))

###############################################################################
# 
# create plot
fig = plt.figure(figsize=(7,7))

# use Cartopy and add features
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(linewidths=0.5)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# plot data
heatmap = t.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), 
                    levels = 40, vmin=0, vmax=32, cmap = 'gist_rainbow_r', 
                    cbar_kwargs={"label":'', "shrink":0.8})

# add colorbar
cbar = plt.colorbar(heatmap, ticks = np.arange(0,32,2))
cbar.ax.set_yticklabels([str(i) for i in np.arange(0,32,2)])

# set axis limits
ax.set_xlim([30,120])
ax.set_ylim([-60,30])

# auto specify ticks
#ax.set_xticks([30, 45, 60, 75, 90, 105, 120], crs=ccrs.PlateCarree())
#ax.set_yticks([-60, -30, 0, 30], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
plt.tick_params(which='both',right=True, top=True)
plt.minorticks_on()

# set titles and axis labels
plt.title('Potential Temperature                  Celsius', fontsize=15)
plt.xlabel('')
plt.ylabel('')

plt.show();