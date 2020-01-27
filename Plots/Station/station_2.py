"""
station_2
=========

Plot random data on US, colored according to value

https://www.ncl.ucar.edu/Applications/Scripts/station_2.ncl
"""
###################################################
# Import necessary packages
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.ticker as tic
import geocat.viz as gcv
import cartopy
import cartopy.crs as ccrs

###################################################
# Define random datasets

# Set up random values
npts = 100
np.random.seed(20200127)
# lat between 25 N and 50 N, lon between 125 W and 70 W
lat = np.random.uniform(25, 50, npts)
lon = np.random.uniform(235, 290, npts)-360
dummy_data = np.random.uniform(-1.2, 35, npts)

###################################################
# Define colormap for plotting

# Set up colormap:
# Need to define boundaries for each color map
# as well as colors for each bin

# Note that len(colors) = len(bin_bounds) + 1
# color[0] => dummy_data < bin_bounds[0]
# color[-1] => dummy_data => bin_bounds[-1]
# color[j] => bin_bounds[j-1] <= dummy_data < bin_bounds[j]

bin_bounds = [0.,5.,10.,15.,20.,23.,26.]
colors = ['purple', 'darkblue', 'blue', 'lightblue', 'yellow', 'orange', 'red', 'pink']

nbins = len(colors) # One bin for each color

# Define colormap for plotting based on these colors
cmap = mpl.colors.ListedColormap(colors)

###################################################
# Both plots rely on same base figure, so
# make a function to create desired plot
# with no legend or colorbar

# Set up figure without colorbar or legend
def make_shared_plot(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax = plt.axes(projection=ccrs.PlateCarree())
    gcv.util.nclize_axis(ax, minor_per_major=5)
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=4))
    gcv.util.add_lat_lon_ticklabels(ax)

    # Set major and minor ticks
    plt.xlim([-125,-70])
    plt.ylim([25,50])
    plt.xticks(range(-120, -75, 20))
    plt.yticks(range(30, 51, 10))

    # Turn on continent shading
    ax.add_feature(cartopy.feature.LAND, edgecolor='lightgray', facecolor='lightgray', zorder=0)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='white', facecolor='white', zorder=0)

    scatter = plt.scatter(lon, lat, c=dummy_data, cmap=cmap, zorder=1)
    return scatter, ax

###################################################
# Make station_2_1 plot

scatter1, ax = make_shared_plot(figsize=(10,5.5))

# add legend
def legend_func(x):
    """
        Returns appropriate legend label
    """
    print(x.shape)
    return()

plt.suptitle('Dummy station data colored according to range of values', y=.9)

# Given how we generated the plot, adding a legend is a little kludgy
# Basically, we draw a second plot where no data is in frame
# but the legend for that plot is drawn where we want it
lax = plt.axes((0, 0, 1, 0.1), frameon=False)
# Plotting window is [0,1] x [0,1]
plt.xlim(0,1)
plt.ylim(0,1)
plt.axis('off')
for n, color in enumerate(colors):
    if n == 0:
        label = f'x < {bin_bounds[0]:.0f}'
    elif n == nbins-1:
        label = f'x >= {bin_bounds[-1]:.0f}'
    else:
        label = f'{bin_bounds[n-1]:.0f} <= x < {bin_bounds[n]:.0f}'
    # Plotting data at (-10, -10) which is not in the plotting window
    scatter = plt.scatter(-10, -10, color=color, label=label)

# The legend for this second plot is what we are actually interested in
# We want large font, no frame around the legend, and 4 columns of labels
lax.legend(loc='center', fontsize='large', frameon=False, ncol=4)

plt.show()

###################################################
# Make station_2_2 plot

scatter2 = make_shared_plot(figsize=(10,5.25))
plt.suptitle('Dummy station data colored according to range of values', y=.9)

# add colorbar
cax = plt.axes((0.225, 0.075, 0.55, 0.025))
norm = mpl.colors.BoundaryNorm([-1.2] + bin_bounds+ [35], len(colors))
cb2 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                norm=norm,
                                boundaries=[-1.2] + bin_bounds + [35],
                                ticks=bin_bounds,
                                orientation='horizontal')
