"""
NCL_polyg_18.py
==============
This script illustrates the following concepts:
   - Adding lines, markers, and polygons to a map
   - Using drawNDCGrid to draw a nicely labeled NDC grid
   - Using "unique_string" to generate unique ids for primitives
   - Drawing lines, markers, polygons, and text in NDC space

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


ax = plt.axes(projection=ccrs.PlateCarree())

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

lon = [-160, -140, -120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120, 140]
lat = [-70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]
marker = ['.', '+', '*', 'o', 'x', 's', '^', 'v', 'D', '>', '<', 'p', 'h', '8', 'X', 'd']
for x in range(len(lon)):
    ax.scatter(lon[x], lat[x], marker=marker[x], color='blue', s=100, zorder = 3)

ax.add_patch(mpatches.Rectangle(xy=[7, 47], width=9, height=7, facecolor='None', edgecolor = 'red', alpha = 1.0, transform=ccrs.PlateCarree(), zorder=5)) 
ax.add_patch(mpatches.Rectangle(xy=[110, -45], width=50, height=35, facecolor='limegreen', alpha = 0.2, transform=ccrs.PlateCarree(), zorder=5)) 

gvutil.add_lat_lon_ticklabels(ax, zero_direction_label=True, dateline_direction_label=True)
gvutil.set_titles_and_labels(ax, maintitle="Big centered title", maintitlefontsize=25)

plt.show()