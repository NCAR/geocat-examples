"""
NCL_native_1.py
===============

This script illustrates the following concepts:
   - Drawing filled contours over a stereographic map
   - Overlaying contours on a map without having latitude and longitude coordinates
   - Setting the view of a stereographic map
   - Turning on map tickmark labels with degree symbols
   - Selecting a different color map
   - Zooming in on a particular area on a stereographic map
   - Using best practices when choosing plot color scheme to accomodate visual impairments

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/native_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/native_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from geocat.viz import util as gvutil
import geocat.datafiles as gdf

###############################################################################
# Read in data:
nlat = 293
nlon = 343

# Read in binary topography file using big endian float data type (>f)
topo = np.fromfile(gdf.get("binary_files/topo.bin"), dtype=np.dtype('>f'))
# Reshape topography array into 2-D array
topo = np.reshape(topo, (nlat,nlon))

# Read in binary latitude/longitude file using big endian float data type (>f)
lat = np.fromfile(gdf.get("binary_files/latlon.bin"), dtype=np.dtype('>f'))
lon = np.fromfile(gdf.get("binary_files/latlon.bin"), dtype=np.dtype('>f'), offset=1)

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=10))

ax.coastlines(linewidths=0.5)

# Set extent to include latitudes from 42 to 49.5 and longitudes from 4 to 16 
ax.set_extent([4, 16, 42, 49.5], ccrs.PlateCarree())

# Draw gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(),
                  draw_labels=True,
                  dms=False,
                  x_inline=False,
                  y_inline=False,
                  linewidth=1,
                  color="black",
                  alpha=0.25)

# Manipulate latitude and longitude gridline numbers and spacing
gl.xlocator = mticker.FixedLocator(np.arange(4, 18, 2))
gl.ylocator = mticker.FixedLocator(np.arange(43, 50))
gl.xlabel_style = {"rotation": 0, "size": 14}
gl.ylabel_style = {"rotation": 0, "size": 14}

gvutil.set_titles_and_labels(ax,
                             lefttitle="topography",
                             lefttitlefontsize=14,
                             righttitle="m",
                             righttitlefontsize=14)
plt.title("Native Sterographic Example",
          loc="center",
          y=1.1,
          size=18,
          fontweight="bold")

# Show the plot
plt.show()


