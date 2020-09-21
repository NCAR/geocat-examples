"""
NCL_panel_2.py
===============
This script illustrates the following concepts:
   - Paneling three plots vertically on a page
   - Adding a common title to paneled plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_2_lg.png
"""

###############################################################################
# Import packages

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

import geocat.datafiles as gdf
import geocat.viz.util as gvutil


###############################################################################
# Import data

# Open netCDF data file using xarray
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)


###############################################################################
# Plot using cartopy and matplotlib

# Generate figure and axes using Cartopy projection
# Make three subplots using matplotlib
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(3, 1, constrained_layout=True, subplot_kw={"projection": projection})

# Set figure size
fig.set_size_inches((8, 13.5))

# Set common plot title
plt.suptitle("A common title", fontsize=16)

# Display continents
continents = cartopy.feature.NaturalEarthFeature(name="coastline", category="physical", scale="50m", edgecolor="None",
                                                 facecolor="lightgray")
[axes.add_feature(continents) for axes in ax.flat]


# Using a dictionary makes it easy to reuse the same keyword arguments twice for the contours
kwargs = dict(
    xticks=np.arange(-180, 181, 30),  # nice x ticks
    yticks=np.arange(-90, 91, 30),  # nice y ticks
    transform=projection,  # ds projection
    add_colorbar=False,  # don't add individual colorbars for each plot call
    add_labels=False,  # turn off xarray's automatic Lat, lon labels
    colors="k",  # note plurals in this and following kwargs
    linestyles="-",
    linewidths=0.5)

# Define first contour levels
levels = np.arange(-16,33,4)

# Panel 1 (Subplot 1)
# Contour-plot U data (for borderlines)
hdl = ds.U.plot.contour(x="lon", y="lat", ax=ax[0], levels=levels, **kwargs)

# Label the contours and set axes title
ax[0].clabel(hdl, np.arange(0, 33, 8), fmt="%.0f")

# Use geocat.viz.util convenience function to add left and right title to the plot axes.
gvutil.set_titles_and_labels(ax[0], lefttitle="Zonal Wind", lefttitlefontsize=12,
                             righttitle=ds.U.units, righttitlefontsize=12)

# Panel 2
# Define second contour levels
levels = np.arange(-10, 50, 2)

# Contour-plot V data (for borderlines)
hdl = ds.V.plot.contour(x="lon", y="lat", ax=ax[1],levels=levels, **kwargs)

# Label the contours and set axes title
ax[1].clabel(hdl, [0], fmt="%.0f")

# Use geocat.viz.util convenience function to add left and right title to the plot axes.
gvutil.set_titles_and_labels(ax[1], lefttitle="Meridional Wind", lefttitlefontsize=12,
                             righttitle=ds.V.units, righttitlefontsize=12)


# Panel 3
# Draw arrows
# xarray doesn't have a quiver method (yet)
# the NCL code plots every 4th value in lat, lon; this is the equivalent of u(::4, ::4)
subset = ds.isel(lat=slice(None, None, 4), lon=slice(None, None, 4))
ax[2].quiver(subset.lon, subset.lat, subset.U, subset.V, width=0.0015, transform=projection, zorder=2, scale=1100)

# Set axes title
ax[2].set_title("Vector Wind", loc="left", y=1.05)

# Use geocat.viz.util convenience function to add left and right title to the plot axes.
gvutil.set_titles_and_labels(ax[2], lefttitle="Vector Wind", lefttitlefontsize=12,
                             righttitle=ds.U.units, righttitlefontsize=12)

# cartopy axes require this to be manual
ax[2].set_xticks(kwargs["xticks"])
ax[2].set_yticks(kwargs["yticks"])

# Use geocat.viz.util convenience function to add minor and major tick lines
[gvutil.add_major_minor_ticks(axes) for axes in ax.flat]

# Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
[gvutil.add_lat_lon_ticklabels(axes) for axes in ax.flat]

# Remove degree markers from x and y labels
[axes.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol='')) for axes in ax.flat]
[axes.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol='')) for axes in ax.flat]


# Display plot
plt.show()


