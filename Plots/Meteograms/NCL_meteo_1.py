"""
NCL_meteo_1.py
===============

This script illustrates the following concepts:
   - Drawing a meteogram
   - Creating a color map using RGB triplets
   - Reversing the Y axis
   - Explicitly setting tickmarks and labels on the bottom X axis
   - Increasing the thickness of contour lines
   - Drawing wind barbs
   - Drawing a bar chart
   - Changing the width and height of a plot
   - Overlaying wind barbs and line contours on filled contours
   - Changing the position of individual plots on a page

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/meteo_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/meteo_1_lg.png
"""

###############################################################################
# Import necessary packages
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.gridspec as gridspec
import cartopy
import cartopy.crs as ccrs
from metpy.calc import smooth_n_point

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/meteo_data.nc"), decode_times=False)

# Extract slice of data
tempisobar = ds.tempisobar
levels = np.sort(np.array(ds.levels).flatten())/10
taus = ds.taus       
rh = ds.rh
ugrid = ds.ugrid
vgrid = ds.vgrid
rain03 = ds.rain03
tempht = ds.tempht

smoothtemp = smooth_n_point(tempisobar, n=5, passes=1)
smoothrh   = smooth_n_point(rh, n=5, passes=1)

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(6,10))

ax1 = fig.add_subplot(311, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313) 

# Generate axes using Cartopy and draw coastlines
ax1.coastlines(linewidths=0.5, alpha=-1)
ax1.set_aspect(1.5)

# Import an NCL colormap
cmap = gvcmaps.wgne15
colors = ListedColormap(np.array(['white', 'honeydew', 'palegreen', 'limegreen', 'green', 'darkgreen']))

bounds = [0, 20, 30, 50, 70, 85]

norm = BoundaryNorm(boundaries=bounds, ncolors=5)

# Plot filled contour
contour1 = ax1.contourf(smoothrh, transform=ccrs.PlateCarree(), cmap=colors, norm=norm,
                          levels=20, zorder=2)

# Plot filled contour
contour2 = ax1.contour(smoothrh, transform=ccrs.PlateCarree(), colors='black',
                          levels=20, linewidths=0.1, zorder=3)

# Plot filled contour
contour3 = ax1.contour(smoothtemp, transform=ccrs.PlateCarree(), colors='red',
                          levels=[0, 5, 10, 20, 30, 40, 50, 60], linewidths=0.4, linestyles='solid', zorder=3)

#ax.clabel(contour2, manual=True)

#X, Y = np.meshgrid(taus, taus)

# Plot barbs
#barbs = ax.barbs(taus, taus, ugrid, vgrid)


gvutil.set_titles_and_labels(ax1, maintitle='Meteogram for LGSA, 28/12Z', maintitlefontsize=18, lefttitle=None, lefttitlefontsize=18, righttitle=None, righttitlefontsize=18,
                          xlabel=None, ylabel='Pressure (mb)', labelfontsize=16)

yticklabels = [1000, 975, 950, 925, 850, 700, 500, 400]

xticklabels = ['12z', '15z', '18z', '21z', 'Apr29', '03z', '06z', '09z', '12z', '15z', '18z',
               '21z', 'Apr30', '03z', '06z', '09z', '12z', '15z', '18z', '21z', 'May01', '03z', '06z', '09z', '12z']

gvutil.set_axes_limits_and_ticks(ax1, xlim=[0,24], ylim=[0,7], xticks=np.arange(0,25), yticks=np.arange(0,8), xticklabels=xticklabels, yticklabels=yticklabels)

for tick in ax1.get_xticklabels():
    tick.set_rotation(90)

# Plot bar chart beneath it

ax2.set_aspect(30)

ax2.bar(taus, rain03, width=3, color='limegreen', edgecolor='k', linewidth=.2)

gvutil.set_titles_and_labels(ax2, ylabel='3hr rain total', labelfontsize=16)

yticklabels = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

xticklabels = ['12z', '', '18z', '', 'Apr29', '', '06z', '', '12z', '', '18z',
               '', 'Apr30', '', '06z', '', '12z', '', '18z', '', 'May01', '', '06z', '', '12z']

gvutil.set_axes_limits_and_ticks(ax2, xlim=[0,72], ylim=[0,.5], xticks=np.arange(0, 75, 3), yticks=np.arange(0,.6,0.1), xticklabels=xticklabels, yticklabels=yticklabels) 

gvutil.add_major_minor_ticks(ax2, y_minor_per_major=5, labelsize="small")

# Plot bar chart beneath it

ax3.set_aspect(2)

ax3.plot(taus, tempht, color='red')

gvutil.set_titles_and_labels(ax3, ylabel='Temp at 2m', labelfontsize=16)

yticklabels = [59, 60, 61, 62, 63, 64]

gvutil.set_axes_limits_and_ticks(ax3, xlim=[0,72], ylim=[59,64.5], xticks=np.arange(0, 75, 3), yticks=np.arange(59,65), xticklabels=xticklabels, yticklabels=yticklabels) 

gvutil.add_major_minor_ticks(ax3, y_minor_per_major=5, labelsize="small")

plt.subplots_adjust(hspace=-0.3)

plt.show()