"""
NCL_station_3.py
================
This script illustrates the following concepts:
   - Drawing station numbers on a map, and removing ones that overlap
   - Attaching lots of text strings to a map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/station_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/station_3_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/station_3_2_lg.png
"""

###################################################
# Import packages:

import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

import geocat.datafiles as gdf

###################################################
# Generate data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = pd.read_csv(
    gdf.get('ascii_files/istasyontablosu_son.txt'),
    delimiter='\\s+',
    names=['index', 'station', 'year1', 'year2', 'number', 'lat', 'lon'])

ncol = 6  # number of columns is 6
npts = len(ds)  # get number of points

# Extract variables
no = ds.index + 1  # +1 because Pandas' RangeIndex start argument defaults to 0
lat = ds.lat
lon = ds.lon

###################################################
# Plot

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 12))

# Generate axes
ax = plt.axes(projection=ccrs.Mercator())

# Set extent to show particular area of the map
ax.set_extent([25.5, 45.2, 35.5, 42.5], ccrs.PlateCarree())

# Add state boundaries other lake features
ax.add_feature(cfeature.LAND, facecolor='none', edgecolor='gray', linewidth=1)

# Add station numbers on the plot
for i in range(len(lat)):
    ax.text(lon[i],
            lat[i],
            no[i],
            fontsize=8,
            fontweight='bold',
            va='center',
            ha='center',
            transform=ccrs.PlateCarree())

# Draw gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(),
                  draw_labels=True,
                  dms=False,
                  x_inline=False,
                  y_inline=False,
                  linewidth=1,
                  color="black",
                  alpha=0.25)

# Set frequency of gridlines in the x and y directions
gl.xlocator = mticker.FixedLocator(np.arange(26, 45, 2))
gl.ylocator = mticker.FixedLocator(np.arange(36, 43, 1))

# Turn off gridlines and top/right labels
gl.xlines = False
gl.ylines = False
gl.top_labels = False
gl.right_labels = False

# Set label sizes
gl.xlabel_style = {"rotation": 0, "size": 14}
gl.ylabel_style = {"rotation": 0, "size": 14}

# Manually turn off ticks on top and right spines
ax.tick_params(axis='x', top=False)
ax.tick_params(axis='y', right=False)

# Add title
ax.set_title('Overlapping text strings', fontweight='bold', fontsize=16, y=1.03)

# Show the plot
plt.tight_layout()
plt.show()
