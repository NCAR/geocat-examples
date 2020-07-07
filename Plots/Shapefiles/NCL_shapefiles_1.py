"""
NCL_shapefiles_1.py
===============
This script illustrates the following concepts:
   - Reading shapefiles
   - Plotting data from shapefiles
   - Using shapefile data to plot unemployment percentages in the U.S.
   - Drawing a custom labelbar on a map
   - Drawing filled polygons over a Lambert Conformal plot
   - Drawing the US with a Lambert Conformal projection
   - Zooming in on a particular area on a Lambert Conformal map
   - Centering the labels under the labelbar boxes

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/shapefiles_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/shapefiles_1_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import shapefile as shp
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open all shapefiles and associated .dbf, .shp, and .prj files so sphinx can run and generate documents
file1 = open(gdf.get("shape_files/states.dbf"), 'r')
file2 = open(gdf.get("shape_files/states.shp"), 'r')
file3 = open(gdf.get("shape_files/states.shx"), 'r')
file4 = open(gdf.get("shape_files/states.prj"), 'r')

# Open shapefiles
shape = shp.Reader(gdf.get("shape_files/states.dbf"))

###############################################################################
# Plot:
plt.figure(figsize=(10,8))
ax = plt.axes(projection=ccrs.LambertConformal(standard_parallels=(33, 45), central_longitude=-98))
ax.set_extent([-125, -64, 22, 50])

ax.add_feature(cfeature.LAND, color='silver')
ax.add_feature(cfeature.LAKES, color='white')

plt.show()
