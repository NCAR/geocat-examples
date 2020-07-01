"""
NCL_panel_13.py
===============
This script illustrates the following concepts:
   - Overlaying a vector field over filled contours
   - Paneling two plots vertically

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_13.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_13_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import xarray as xr
import math

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))

# Extract data from second timestep
ds = ds.isel(time=1).drop_vars('time')
U = ds.U[::4]
V = ds.V[::4]

# Calculate the magnitude of the winds
magnitude = np.sqrt(U.data**2 + V.data**2)

###############################################################################
# Plot:

# Create sublots and specify their projections
projection = ccrs.PlateCarree()
fig, axs = plt.subplots(2, 1, figsize=(8, 10), subplot_kw={"projection": projection}, gridspec_kw={'hspace': 0.3})

# Add coastlines
axs[0].coastlines(linewidth=0.5)
axs[1].coastlines(linewidth=0.5)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(axs[0], xticks=np.arange(-180, 181, 30),
                                 yticks=np.arange(-90, 91, 30))
gvutil.set_axes_limits_and_ticks(axs[1], xticks=np.arange(-180, 181, 30),
                                 yticks=np.arange(-90, 91, 30))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axs[0])
gvutil.add_major_minor_ticks(axs[1])

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(axs[0])
gvutil.add_lat_lon_ticklabels(axs[1])

# Use geocat.viz.util convenience function to add main title as well as titles to left and right of the plot axes.
gvutil.set_titles_and_labels(axs[0], lefttitle='Speed', lefttitlefontsize=10,
                             righttitle=U.units, righttitlefontsize=10)
gvutil.set_titles_and_labels(axs[1], lefttitle='Wind', lefttitlefontsize=10,
                             righttitle=U.units, righttitlefontsize=10)


# Load in colormap
newcmap = gvcmaps.gui_default

# Specify contour levels and contour ticks
speed_levels = np.arange(0, 40, 2.5)
speed_ticks = np.arange(2.5, 37.5, 2.5)
wind_levels = np.arange(-16, 44, 4)
wind_ticks = np.arange(-12, 40, 4)

# Plot filled contours
speed = axs[0].contourf(U['lon'], U['lat'], magnitude, levels=speed_levels, cmap=newcmap)
speed_cbar = plt.colorbar(speed, ax=axs[0], orientation='horizontal', ticks=speed_ticks, shrink=0.75, drawedges=True)

wind = axs[1].contourf(U['lon'], U['lat'], U.data, levels=wind_levels, cmap=newcmap)
plt.colorbar(wind, ax=axs[1], orientation='horizontal', ticks=wind_ticks, shrink=0.75, drawedges=True)

# Remove trailing zeros from speed color bar tick labels
speed_cbar.ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))

plt.show()
