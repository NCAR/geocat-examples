"""
NCL_lcnative_1_lg.py
================

This script illustrates the following concepts:
    - Drawing contours over a map using a native lat,lon grid
    - Drawing filled contours over a Lambert Conformal map
    - Zooming in on a particular area on a Lambert Conformal map
    - Subsetting a color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lcnative_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lcnative_1_lg.png
"""

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"), decode_times=False)

# Extract a slice of the data
t = ds.pre[0,:]
print(ds)
#gvutil.xr_add_cyclic_longitudes(t,'lon')

###############################################################################
# Plot:

# Generate figure
plt.figure(figsize=(10, 10))


# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=45, standard_parallels=(36,55))
ax = plt.axes(projection=projection, frameon=True)
ax.set_extent((30, 55, 20, 45), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')

gl.left_labels = True
gl.bottom_labels = False
gl.xlines = False
gl.xlocator = mticker.FixedLocator([30, 35, 40, 45, 50, 55])
#gl.xformatter = LONGITUDE_FORMATTER
#gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 15, 'color': 'gray'}
gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

ax.plot(np.arange(30,55,5))


# Plot data and create colorbar
newcmp = gvcmaps.BlueYellowRed
t.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), levels = 14, cbar_kwargs={"orientation":"horizontal",  "ticks":np.arange(0, 240, 20),  "label":'', "shrink":0.9})

# Use geocat.viz.util convenience function to add minor and major tick lines
#Use geocat.viz.util convenience function to set axes tick values
#gvutil.set_axes_limits_and_ticks(ax, xticks=np.linspace(30, 55, 6), yticks=np.linspace(20, 45, 6))

#Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
#gvutil.add_lat_lon_ticklabels(ax)

#Use geocat.viz.util convenience function to add minor and major tick lines
#gvutil.add_major_minor_ticks(ax, labelsize=12)

#Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
#gvutil.set_titles_and_labels(ax, lefttitle='Anomalies: Surface Temperature', righttitle='K')

plt.title(t.long_name, loc='left', size=16)
plt.title(t.units, loc='right', size=16)





plt.show()

