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

import geocat.viz as gv

###############################################################################
# Create dummy data

lat = np.arange(-75, 90, 20)  #np.random.uniform(-80, 80, 20)
lon = np.arange(-170, 180, 20)  #np.random.uniform(-170, 170, 20)

###############################################################################
# Plot

# Generate a figure and axes
plt.figure(figsize=(10, 9))

projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

# Add coastlines to plot
ax.coastlines()

# Create an array of colors
colors = ['blue', 'green', 'red', 'yellow', 'purple']

for i in range(len(lat)):
    for j in range(len(lon)):
        ax.scatter(lon[j],
                   lat[i],
                   color=np.random.choice(colors, size=1)[0],
                   s=900,
                   linewidths=1,
                   alpha=0.75,
                   zorder=2,
                   marker='s')

# plt.xlim(-180, 190)
# plt.ylim(-90, 90)

gv.set_axes_limits_and_ticks(ax,
                             xlim=(-180, 190),
                             ylim=(-90, 100),
                             xticks=np.arange(-180, 190, 30),
                             yticks=np.arange(-90, 100, 30))

gv.add_lat_lon_ticklabels(ax)
