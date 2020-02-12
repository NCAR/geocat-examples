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
                    add_colorbar=False)

# add colorbar
cbar = plt.colorbar(heatmap, ticks = np.arange(0,32,2))
cbar.ax.set_yticklabels([str(i) for i in np.arange(0,32,2)])

# set axis limits
ax.set_xlim([30,120])
ax.set_ylim([-60,30])

# manually specify ticks
#xticks = [30, 60, 90, 120]
#xlabels = ['30E', '60E', '90E', '120E']
#yticks = [-60, -30, 0, 30]
#ylabels = ['60S', '30S', '0', '30N']
#plt.xticks(xticks, xlabels)
#plt.yticks(yticks, ylabels)
plt.tick_params(which='both',right=True, top=True)
plt.minorticks_on()

# set titles and axis labels
plt.subtitle('Drefault map tickmark labels')
plt.title('Potential Temperature                  Celsius', fontsize=15)
plt.xlabel('')
plt.ylabel('')

plt.show();