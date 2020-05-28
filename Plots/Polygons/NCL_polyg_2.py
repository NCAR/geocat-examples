"""
NCL_polyg_2.py
==============
Concepts illustrated:
  - Drawing a Lambert Conformal U.S. map color-coded by climate divisions
  - Color-coding climate divisions based on precipitation values
  - Drawing the climate divisions of the U.S.
  - Zooming in on a particular area on a Lambert Conformal map
  - Drawing filled polygons on a map
  - Drawing a border around filled polygons
  - Masking the ocean in a map plot
  - Masking land in a map plot
  - Increasing the font size of text
  - Adding text to a plot
  - Drawing a custom labelbar on a map
  - Creating a red-yellow-blue color map 

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polyg_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polyg_2_lg.png
"""

###############################################################################
# Import packages:
# ----------------
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
import cartopy.io.shapereader as shpreader

###############################################################################

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())

ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m',
                                     category='cultural', name=shapename)

ax.set_title("Average Annual Precipiation \n Computed for the period 1899-1999 \n NCDC climate division data")
ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)

for state in shpreader.Reader(states_shp).geometries():
    
    facecolor = 'white'
    edgecolor = 'black'

    ax.add_geometries([state], ccrs.PlateCarree(),
                      facecolor=facecolor, edgecolor=edgecolor)

plt.show()