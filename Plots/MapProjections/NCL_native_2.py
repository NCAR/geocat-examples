"""
NCL_native_2.py
================

This script illustrates the following concepts:
   - Drawing filled contours over a mercator map
   - Overlaying contours on a map without having latitude and longitude coordinates
   - Turning on map tickmark labels with degree symbols
   - Selecting a different color map
   - Zooming in on a particular area on a mercator map
   - Using best practices when choosing plot color scheme to accomodate visual impairments

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/native_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/native_2_lg.png
"""

###############################################################################

# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import geocat.datafiles as gdf

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and
# load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/1994_256_FSD.nc"),
                     decode_times=False)
t = ds.FSD.isel(time=0)

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines(linewidths=0.5)
ax.add_feature(cfeature.LAND, facecolor="lightgray")

# Set extent to include latitudes from 34 to 52 and longitudes from 128
# to 144
ax.set_extent([128, 144, 34, 52], ccrs.PlateCarree())

# Contourf-plot data (for filled contours)
pt = t.plot.contourf(ax=ax,
                     transform=ccrs.PlateCarree(),
                     vmin=0,
                     vmax=70,
                     levels=15,
                     cmap="inferno",
                     cbar_kwargs={
                         "extendrect": True,
                         "orientation": "vertical",
                         "ticks": np.arange(0, 71, 5),
                         "label": ""
                     })

# Draw gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(),
                  draw_labels=True,
                  dms=False,
                  x_inline=False,
                  y_inline=False,
                  linewidth=1,
                  color="k",
                  alpha=0.25)

# Manipulate latitude and longitude gridline numbers and spacing
gl.top_labels = False
gl.right_labels = False
gl.xlocator = mticker.FixedLocator([130, 134, 138, 142])
gl.ylocator = mticker.FixedLocator([36, 38, 40, 42, 44, 46, 48, 50])
gl.xlabel_style = {"rotation": 0, "size": 15}
gl.ylabel_style = {"rotation": 0, "size": 15}

plt.title("Native Mercator Projection",
          loc="center",
          y=1.05,
          size=15,
          fontweight="bold")
plt.title(t.units, loc="right", y=1.0, size=14)
plt.title("free surface deviation", loc="left", y=1.0, size=14)

# Show the plot
plt.show()
