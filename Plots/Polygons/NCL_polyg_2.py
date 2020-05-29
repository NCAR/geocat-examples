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
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import matplotlib.cm as cm

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom

###############################################################################

statenames = ["AL","AR","AZ","CA","CO","CT","DE","FL","GA","IA","ID","IL",
  "IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT",
  "NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA",
  "RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]

ncds = [8,9,7,7,5,3,2,6,9,9,10,9,9,9,4,9,3,8,3,10,9,6,10,7,
  8,9,8,2,3,8,4,10,10,9,9,10,1,7,9,4,10,7,7,3,10,9,6,10]

colormap = {1:'mediumpurple', 2:'mediumblue', 3:'royalblue',
            4:'cornflowerblue', 5:'lightblue', 6:'teal', 7:'yellowgreen', 8:'green', 
            9:'wheat', 10:'tan', 11:'gold', 12:'orange', 13:'red', 14:'firebrick'}

###############################################################################

fig = plt.figure(figsize=(10,10))

ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
ax.set_extent([-125, -65.0, 24, 50], ccrs.Geodetic())

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

ds = xr.open_dataset(gdf.get("netcdf_files/climdiv_polygons.nc"))

print(ds.get('CA_CD5'))
for varname, da in ds.data_vars.items():
    
  first = ds.get(varname)
  lat = first.lat
  lon = first.lon

  track = sgeom.LineString(zip(lon, lat))
  im = ax.add_geometries([track], ccrs.PlateCarree(), facecolor=colormap[np.random.randint(1, 14)], edgecolor='k', linewidths=.5)

# Make colorbar
fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)

cmap = colors.ListedColormap(['mediumpurple', 'mediumblue', 'royalblue',
            'cornflowerblue', 'lightblue', 'teal', 'yellowgreen', 'green', 
            'wheat', 'tan', 'gold', 'orange', 'red', 'firebrick'])

bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45 ,50, 60, 70, 80 , 90]
norm = colors.BoundaryNorm(bounds, cmap.N)
fig.colorbar(
    cm.ScalarMappable(cmap=cmap, norm=norm),
    cax=ax,
    boundaries=bounds,
    ticks=bounds,
    spacing='uniform',
    orientation='horizontal',
    label='inches',
)

plt.show()