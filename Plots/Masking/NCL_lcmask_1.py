"""
NCL_lcmask_1.py
===============
This script illustrates the following concepts:
   - Drawing filled contours over a Lambert Conformal map
   - Zooming in on a particular area on a Lambert Conformal map
   - Creating a custom plot boundary
   - Using a blue-white-red color map
   - Setting contour levels using a min/max contour level and a spacing

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://ncl.ucar.edu/Applications/Scripts/lcmask_1.ncl
    - Original NCL plot: http://ncl.ucar.edu/Applications/Images/lcmask_1_1_lg.png and http://ncl.ucar.edu/Applications/Images/lcmask_1_2_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Utility function to create a wedge shaped path for plot boundary:
def wedge_boundary(ax, lon_range, lat_range, res=1):
    """
    Utility function to create a custom wedge shaped map boundary using given
    ranges of longitudes and latitudes.

    Args:

        ax (:class:'matplotlib.axes'):
            The axes to which the boundary will be applied.

        lon_range (:class:'tuple'):
            The two-tuple containting the start and end of the desired range of
            longitudes. The first entry must be smaller than the second entry.
            Both entries must be between [-180 , 180].

        lat_range (:class:'tuple'):
            The two-tuple containting the start and end of the desired range of
            longitudes. The first entry must be smaller than the second entry.
            Both entries must be between (-90 , 90).

        res (:class:'int'):
            The size of the incrementation for vertices in degrees. Default is
            a vertex every one degree of longitude.

    """

    # Set extent of map
    ax.set_extent([lon_range[0], lon_range[1], lat_range[0], lat_range[1]],
                  ccrs.PlateCarree())
    # Make a boundary path in PlateCarree projection begining in the bottom
    # left and continuing anitclockwise creating a point every `res` degree
    vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], lon_range[1] + 1, res)] + \
               [(lon, lat_range[1]) for lon in range(lon_range[1], lon_range[0] - 1, -res)]
    boundary = mpath.Path(vertices)
    ax.set_boundary(boundary, transform=ccrs.PlateCarree())


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays and disable time decoding due to missing necessary metadata
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
# Extract a slice of the data
ds = ds.isel(time=0).drop_vars(names=["time"])
ds = ds.isel(lev=0).drop_vars(names=["lev"])
V = ds.V
# Ensure longitudes range from 0 to 360 degrees
V = gvutil.xr_add_cyclic_longitudes(V, "lon")

###############################################################################
# Plot unmasked data:

# Generate figure and projection using Cartopy
plt.figure(figsize=(7, 10))
proj = ccrs.LambertConformal(central_longitude=0,
                                   standard_parallels=(45, 89))
# Set axis projection
ax = plt.axes(projection=proj, frameon=False)
# Set extent to include all longitudes and the northern hemisphere
ax.set_extent((0, 359, 0, 89), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)


# Plot data and create colorbar
newcmp = gvcmaps.BlWhRe

wind = V.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(),
                       add_colorbar=False, levels=24)
cbar = plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True,
             ticks=np.arange(-48, 48, 8), pad=0.1, aspect=12)
cbar.ax.tick_params(length=0) # remove tick marks but leave in labels

# Use geocat.viz.util convenience function to add left and right titles
gvutil.set_titles_and_labels(ax, lefttitle=V.long_name, lefttitlefontsize=16,
                             righttitle=V.units, righttitlefontsize=16)

plt.show()

###############################################################################
# Mask data
masked = V.where(V.lat > 20)
masked = masked.where(masked.lat < 80)
masked = masked.where(masked.lon > 90)
masked = masked.where(masked.lon < 220)

# Rotate data to match NCL example
masked['lon'] = masked['lon'] + 180

###############################################################################
# Plot masked data

# Generate figure and projection using Cartopy
plt.figure(figsize=(10, 7))
proj = ccrs.LambertConformal(central_longitude=-22.5,
                             standard_parallels=(45, 89))
# Set axis projection
ax = plt.axes(projection=proj)
ax.coastlines(linewidth=0.5)

# Make a custom boundary using convenience function
wedge_boundary(ax, [-85, 40], [20, 80])

# Plot data and create colorbar
wind = masked.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(),
                            add_colorbar=False, levels=24)
cbar = plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True,
             ticks=np.arange(-40, 44, 4), pad=0.1, aspect=18)
cbar.ax.tick_params(length=0) # remove tick marks but leave in labels

# Use geocat.viz.util convenience function to add left and right titles
gvutil.set_titles_and_labels(ax, lefttitle=V.long_name, lefttitlefontsize=16,
                             righttitle=V.units, righttitlefontsize=16)
plt.show()
