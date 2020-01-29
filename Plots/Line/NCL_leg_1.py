"""
leg_1.py
===============
Plots/Lines/Legends
"""

###############################################################################
# 
# import modules
import xarray as xr
import matplotlib.pyplot as plt


###############################################################################
# 
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/uv300.nc')
uz = ds.U.isel(time=0).mean(dim=['lon'])
vz = ds.V.isel(time=0).mean(dim=['lon'])

###############################################################################
# 
# create plot
plt.figure(figsize=(5,5))
plt.plot(vz.lat, vz.values, '--', c='gray', label='V')
plt.plot(uz.lat, uz.values, c='gray', label='U')

# specify X and y axis limits
plt.ylim([-10,40])
plt.xlim([-90,90])

# specify axis ticks
xticks = [-90, -60, -30, 0, 30, 60, 90]
xlabels = ['90S', '60S', '30S', '0', '30N', '60N', '90N']
plt.xticks(xticks, xlabels)
plt.minorticks_on()
plt.tick_params(which='both',right=True, top=True)

# demonstrate adjusting legend location, frame, and font
plt.legend(loc='upper left', frameon=False, prop={'weight':'bold'})

plt.show();

