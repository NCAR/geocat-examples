"""
NCL_polyg_18.py
==============
This script illustrates the following concepts:
   - Adding lines, markers, and polygons to a map
   - Drawing lines, markers, polygons, and text in inset axes

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polyg_18.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polyg_18_2_lg.png
"""

###############################################################################
# Import packages:
# ----------------
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy
from geocat.viz import util as gvutil
import matplotlib.patches as mpatches
###############################################################################
# Define helper function to remove ticks/frames from axes

def removeTicks(axis):
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)

###############################################################################
# Plot map, markers, and polygons

# Set size of figure
fig = plt.figure(figsize=(10,10))

# Make grid on figure with 2 rows, 1 column
grid = plt.GridSpec(2, 20, hspace=0.2, wspace=0.2, figure=fig)

# Make subplot for map
ax = plt.subplot(grid[:-1, 1:], projection=ccrs.PlateCarree())

# Add continents
continents = cartopy.feature.NaturalEarthFeature(
        name="coastline",
        category="physical",
        scale="50m",
        edgecolor="None",
        facecolor="lightgray",
)
ax.add_feature(continents)

# Set map extent
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

# Create arrays with location and design of each marker
lon = [-160, -140, -120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120, 140]
lat = [-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
marker = ['.', '+', '*', 'o', 'x', 's', '^', 'v', 'D', '>', '<', 'p', 'h', '8', 'X', 'd']

# Draw markers on diagonal line across graph
for x in range(len(lon)):
    ax.scatter(lon[x], lat[x], marker=marker[x], color='blue', s=100, zorder = 3)

# Draw small red box in upper center
ax.add_patch(mpatches.Rectangle(xy=[7, 47], width=9, height=7, facecolor='None', edgecolor = 'red', alpha = 1.0, transform=ccrs.PlateCarree(), zorder=5)) 

# Draw green window in bottom right
ax.add_patch(mpatches.Rectangle(xy=[110, -45], width=50, height=35, facecolor='lime', alpha = 0.3, transform=ccrs.PlateCarree(), zorder=5)) 

# Use gvutil function to set the ticks on axes
gvutil.set_axes_limits_and_ticks(ax, xlim=None, ylim=None, xticks=[-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180], yticks=[-90, -60, -30, 0, 30, 60, 90], xticklabels=None, yticklabels=None)

# Use gvutil function to give ticks W/N/E/S labels
gvutil.add_lat_lon_ticklabels(ax, zero_direction_label=True, dateline_direction_label=True)

# Use gvutil function to set title of plot
gvutil.set_titles_and_labels(ax, maintitle="Big centered title", maintitlefontsize=25)

# Use gvutil function to plot three minor ticks for every major tick on axes
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=3, labelsize="small")

###############################################################################
# Plot legend

# Create second plot for legend
ax2 = plt.subplot(grid[-1, 1:], frameon=False)
removeTicks(ax2)

# Create 6 inset axes within subplot for each field in legend
# Inset_axes positional array argument takes four values: 
# [starting (bottom left) x coordinate of window, starting y coordinate of window, width of field, height of field]

# Add circle image
axin1 = ax2.inset_axes([0.1, 0.8, .1, .1], frameon=False)
removeTicks(axin1)
axin1.add_patch(mpatches.Circle((0.1, 0.1), radius=.1,color='blue'))
axin1.axis('equal')

# Add label for circle
axin2 = ax2.inset_axes([0.0, 0.65, .20, .5], frameon=False)
removeTicks(axin2)
axin2.text(0,.7,'Marker (left justified text)', color='blue', fontsize=12, verticalalignment='center')

# Add red line
axin3 = ax2.inset_axes([0.30, 0.6, .33, .5], frameon=False)
removeTicks(axin3)
axin3.plot([0, 4], [3, 3], color='red')
axin1.axis('scaled')

# Add label for red line
axin4 = ax2.inset_axes([0.33, 0.65, .33, .5], frameon=False)
removeTicks(axin4)
axin4.text(0,.7,'Polyline (centered text)', color='red', fontsize=12,  verticalalignment='center')

# Add green polygon 
axin5 = ax2.inset_axes([0.62, 0.6, .33, .5], frameon=False)
removeTicks(axin5)
axin5.add_patch(mpatches.Rectangle(xy=[.3, .3], width=.6, height=.3, facecolor='lime', alpha = 0.3))
axin1.axis('scaled')

# Add label for green polygon
axin6 = ax2.inset_axes([0.66, 0.65, .33, .5], frameon=False)
removeTicks(axin6)
axin6.text(0,.7,'Polygon (right justified text)', color='lime', fontsize=12, verticalalignment='center')

plt.show()