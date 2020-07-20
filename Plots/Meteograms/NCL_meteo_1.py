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
levels = ds.levels
taus = ds.taus
rh = ds.rh
ugrid = ds.ugrid
vgrid = ds.vgrid
rain03 = ds.rain03
tempht = ds.tempht

smoothtemp = smooth_n_point(tempisobar, n=5, passes=1)
smoothrh   = smooth_n_point(rh, n=5, passes=1)
smoothtemp=tempisobar
smoothrh=rh

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(6,10))

ax1 = fig.add_subplot(311, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(312)

# Generate axes using Cartopy and draw coastlines
ax1.coastlines(linewidths=0.5, alpha=-1)
ax1.set_aspect(1.5)

# Import an NCL colormap
cmap = gvcmaps.wgne15
colors = ListedColormap(np.array(['white', 'honeydew', 'palegreen', 'limegreen', 'green', 'darkgreen']))

bounds = [-20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

norm = BoundaryNorm(boundaries=bounds, ncolors=5)

# Plot filled contour
contour1 = ax1.contourf(smoothrh, transform=ccrs.PlateCarree(), cmap=colors, norm=norm,
                          levels=bounds, zorder=2)

# Plot filled contour
contour2 = ax1.contour(smoothrh, transform=ccrs.PlateCarree(), colors='black',
                          levels=bounds, linewidths=0.1, zorder=3)

# Plot filled contour
contour3 = ax1.contour(smoothtemp, transform=ccrs.PlateCarree(), colors='red',
                          levels=[-20, -10, 0, 10, 20, 30, 40, 50, 60], linewidths=0.4, linestyles='solid', zorder=4)

cont2Labels = [(1.71, 3.82), (5.49, 3.23), (9.53, 4.34), (9.27, 3.53), (14.08, 4.81),
               (19.21, 2.24), (17.74, 1.00), (22.23, 3.87), (12.87, 2.54), (10.45, 6.02),
               (11.51, 4.92)]

cont3Labels = [(7.5, 6.1), (10.0, 4.58), (19.06, 1.91), (8.68, 0.46), (19.52, 4.80),
               (16.7, 6.07), (8.62, 5.41), (18.53, 5.46)]

cont2labels = ax1.clabel(contour2, manual=cont2Labels, fmt='%d', inline=True, fontsize=7)
cont3labels = ax1.clabel(contour3, manual=cont3Labels, fmt='%d', inline=True, fontsize=7, colors='k')

# Set label backgrounds white
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=.5)) for txt in contour2.labelTexts]
[txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=.5)) for txt in contour3.labelTexts]

# Plot barbs
barbs = ax1.quiver(taus, levels, ugrid, vgrid, color='k', pivot='middle', zorder=5)
#transform=ccrs.PlateCarree(), 

gvutil.set_titles_and_labels(ax1, maintitle='Meteogram for LGSA, 28/12Z', maintitlefontsize=18, ylabel='Pressure (mb)', labelfontsize=12)

yticklabels = np.array(levels)

xticklabels = ['12z', '15z', '18z', '21z', 'Apr29', '03z', '06z', '09z', '12z', '15z', '18z',
               '21z', 'Apr30', '03z', '06z', '09z', '12z', '15z', '18z', '21z', 'May01', '03z', '06z', '09z', '12z']

gvutil.set_axes_limits_and_ticks(ax1, xlim=[0,24], ylim=[0,7], xticks=np.arange(0,25), yticks=np.arange(0,8), xticklabels=xticklabels, yticklabels=yticklabels)

ax1.tick_params(axis="x", direction="in")
ax1.tick_params(axis="y", labelsize=9) 
ax1.yaxis.labelpad = -3
for tick in ax1.get_xticklabels():
    tick.set_rotation(90)

# Create text box
ax1.text(1.0, -0.35, "CONTOUR FROM -20 TO 60 BY 10",
        horizontalalignment='right',
        transform=ax1.transAxes,
        bbox=dict(boxstyle='square, pad=0.15', facecolor='white', edgecolor='black'))

# Create inset axes below first axes
axin1 = ax2.inset_axes([0.0, 0.3, 1, 0.30])
axin2 = ax2.inset_axes([0.0, -.1, 1, 0.35])
ax2.axis("off")

# Plot bar chart

axin1.set_aspect(30)

axin1.bar(taus, rain03, width=3, color='limegreen', edgecolor='k', linewidth=.2)

gvutil.set_titles_and_labels(axin1, ylabel='3hr rain total', labelfontsize=12)

yticklabels = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

xticklabels = ['12z', '', '18z', '', 'Apr29', '', '06z', '', '12z', '', '18z',
               '', 'Apr30', '', '06z', '', '12z', '', '18z', '', 'May01', '', '06z', '', '12z']

gvutil.set_axes_limits_and_ticks(axin1, xlim=[0,72], ylim=[0,.5], xticks=np.arange(0, 75, 3), yticks=np.arange(0,.6,0.1), xticklabels=xticklabels, yticklabels=yticklabels) 

gvutil.add_major_minor_ticks(axin1, y_minor_per_major=5, labelsize="small")
axin1.tick_params(bottom=True, left=True, right=True, top=False)
axin1.tick_params(which='minor', top=False)

# Plot line chart beneath it

axin2.set_aspect(2)

axin2.plot(taus, tempht, color='red')

gvutil.set_titles_and_labels(axin2, ylabel='Temp at 2m', labelfontsize=12)

yticklabels = [59, 60, 61, 62, 63, 64]

gvutil.set_axes_limits_and_ticks(axin2, xlim=[0,72], ylim=[59,64.5], xticks=np.arange(0, 75, 3), yticks=np.arange(59,65), xticklabels=xticklabels, yticklabels=yticklabels) 

gvutil.add_major_minor_ticks(axin2, y_minor_per_major=5, labelsize="small")
axin2.tick_params(bottom=True, left=True, right=True, top=False)
axin2.tick_params(which='minor', top=False)

plt.subplots_adjust(hspace=-0.3)

plt.show()