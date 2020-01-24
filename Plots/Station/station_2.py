"""
station_2
=========

Plot random data on US, colored according to value

https://www.ncl.ucar.edu/Applications/Scripts/station_2.ncl
"""
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.ticker as tic
import geocat.viz as gcv
import cartopy
import cartopy.crs as ccrs

###################################################

# bin settings (bin0 = < 0., bin1 = 0.:4.999, etc.)
arr = np.array([0.,5.,10.,15.,20.,23.,26.])
nbins = len(arr) + 1

# Set up random values
npts = 100
np.random.seed(20200124)
lat = np.random.uniform(25, 50, npts)
lon = np.random.uniform(235, 290, npts)-360
dummy_data = np.random.uniform(-1.2, 35, npts)

###################################################

# Define colors that we want to use for different ranges
# Note that len(colors) = len(arr) + 1
# color[0] => dummy_data < arr[0]
# color[-1] => dummy_data => arr[-1]
# color[j] => arr[j-1] <= dummy_data < arr[j]
colors = ['purple', 'darkblue', 'blue', 'lightblue', 'yellow', 'orange', 'red', 'pink']

# color_table is an array of colors for each point
color_table =np.empty(npts, str)
for j in range(nbins):
    if j == 0:
        indices = dummy_data < arr[0]
    elif j < len(arr):
        indices = (dummy_data >= arr[j-1]) & (dummy_data < arr[j])
    else: # j == len(arr)
        indices = dummy_data >= arr[-1]
    color_table = np.where(indices, colors[j], color_table)

###################################################

# Sanity check for comparing against the plot
# 1. Is color correct for given value?
# 2. Is dot at given (lon, lat) correct?

for i in range(0,100,10):
    print(f'({lon[i]:0.2f}, {lat[i]:0.2f}): val = {dummy_data[i]:0.1f} => {color_table[i]} dot')

###################################################

# Set up figure
fig, ax = plt.subplots(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree())
gcv.util.nclize_axis(ax, minor_per_major=5)
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=4))
gcv.util.add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xlim([-130,-60])
plt.ylim([25,50])
plt.xticks(range(-120, -75, 20))
plt.yticks(range(30, 51, 10))

# Turn on continent shading
ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=0)
ax.add_feature(cartopy.feature.LAKES, edgecolor='white', facecolor='white', zorder=0)

scatter = plt.scatter(lon, lat, c=color_table, zorder=1)
plt.title('Dummy station data colored according to range of values')
# colorbar
cax = plt.axes((0.225, 0.125, 0.55, 0.025))
cmap = mpl.colors.ListedColormap(colors)
norm = mpl.colors.BoundaryNorm([-1.2] + list(arr)+ [35], len(colors))

cb2 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                norm=norm,
                                boundaries=[-1.2] + list(arr)+ [35],
                                ticks=arr,
                                orientation='horizontal')
