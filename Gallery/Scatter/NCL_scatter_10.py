"""
NCL_scatter_10.py
=================
This script illustrates the following concepts:
   - Drawing a scatter plot over a map using the "overlay" procedure
   - Using gsn_csm_blank_plot to create a scatter plot with filled polygons
   - Generating dummy data using "random_uniform"
   - Changing the draw order of filled polygons

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/scatter_10.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/scatter_10_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.viz as gv

###############################################################################
# Create dummy data

lat = np.arange(-70, 85, 20)
lon = np.arange(-160, 170, 20)

###############################################################################
# Plot

# Generate a figure and axes
plt.figure(figsize=(12, 10))

projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Add coastlines to plot
ax.coastlines()

# Create an array of colors
colors = ['blue', 'green', 'red', 'yellow', 'purple']

# Plot random markers on the map
for i in range(len(lat)):
    for j in range(len(lon)):
        # Generate a random number between 0 and 1
        rand = np.random.random(size=1)

        # Don't plot a marker if rand<0.35 (exit the loop)
        if rand < 0.35:
            continue

        # Scatter plot
        ax.scatter(
            lon[j],  # Longitude of marker
            lat[i],  # Latitude of marker
            color=np.random.choice(colors,
                                   size=1)[0],  # Randomly select a color
            s=1230,  # Size of marker
            alpha=0.75,  # Transparency of the marker
            zorder=2,  # PLot markers on top of map
            marker='s')  # Use a square shaped marker

gv.add_lat_lon_ticklabels(ax)

ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

gv.add_major_minor_ticks(ax, labelsize=14)
gv.set_axes_limits_and_ticks(ax=ax,
                             xlim=(-180, 190),
                             ylim=(-90, 100),
                             xticks=np.arange(-180, 190, 30),
                             yticks=np.arange(-90, 100, 30))

plt.title('Dummy markers over a map', fontweight='bold', fontsize=20)
