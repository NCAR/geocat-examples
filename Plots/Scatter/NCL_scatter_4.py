"""
==========
scatter_4
==========
Plots/Scatter/Lines
"""

################################################################################
#
# import modules
#
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


################################################################################
#
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/b003_TS_200-299.nc', decode_times=False)
ts = ds.TS.sel(lat = 60, lon = 180, method = 'nearest')

###############################################################################
# 
# smooth data so that seasonal cycle is less 
# prominent. This is for demo purposes only 
# so that the regression line is more sloped.
ts_rolled = ts.rolling(time=40, center=True).mean().dropna('time')

###############################################################################
# 
# calculate regression line
m, b = np.polyfit(ts_rolled.time, ts_rolled.values, 1)
regline_vals = [m * x + b for x in ts.time]

###############################################################################
# 
# create plot
plt.figure(figsize=(6,6))
plt.scatter(ts_rolled.time, ts_rolled.values, c='r', s=3)
plt.plot(ts.time, regline_vals, 'k')

# specify X and Y axis limits
plt.xlim([6000, 9500])
plt.ylim([268.0, 271.5])

# specify tick parameters
plt.tick_params(which='both',right=True, top=True)
plt.minorticks_on()

# adjust title and axis labels
plt.title('Output from regline')
plt.xlabel('simulated time')
plt.ylabel('Surface temperature')

plt.show();