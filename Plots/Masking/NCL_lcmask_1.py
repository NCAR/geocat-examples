"""
NCL_lcmask_1.py
===============
This script illustrates the following concepts:
   - Drawing filled contours over a Lambert Conformal map
   - Drawing a filled contours over a masked Lambert Conformal plot
   - Zooming in on a particular area on a Lambert Conformal map
   - Creating a custom plot boundary
   - Using a blue-white-red color map
   - Setting contour levels using a min/max contour level and a spacing
   - Turning off the addition of a longitude cyclic point

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
import math

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Defining a utility function to create a wedge shaped path for plot boundary


def wedge_path(theta1, theta2, r, width=None, center=(0, 0), res=100):
    """
    Utility function to create a wedge shaped path of radius r sweeping from
    theta1 to theta2.

    Args:

        theta1 (:class:'float'):
            Angle right of the verticle in degrees where the wedge will begin.

        theta2 (:class:'float'):
            Angle right fo the verticle in degrees where the wedge will end.

        r (:class:'float'):
            Radius of the wedge

        width (:class:'float'):
            Width of the partial wedge with inner radius r - width and outer
            radius r.

        center (:class:'tuple'):
            Positon of the wedge relative to lower left corner of axes.

        res (:class:'int'):
            Resolution of the vertices. A higher number results in smoother
            arcs.

    """

    # Start and end angles of the wedge
    start = math.radians(theta1)
    end = math.radians(theta2)
    theta = np.linspace(start, end, res)

    # Calculating vertices for each arc
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    outer = verts * r + center
    if width is None:
        inner = np.full_like(verts, center)
    else:
        inner = verts * (r - width) + center

    # Flip to ensure the end of one arc is connected to the start of the other
    outer = np.flip(outer, axis=0)

    # Appending the list of arc vertices and creating a path object
    points = np.append(inner, outer, axis=0)
    wedge = mpath.Path(points)

    return wedge


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays and disable time decoding due to missing necessary metadata
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
# Extract a slice of the data
ds = ds.isel(time=0).drop("time")
ds = ds.isel(lev=0).drop("lev")
V = ds.V

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
V = gvutil.xr_add_cyclic_longitudes(V, "lon")

###############################################################################
# Plot unmasked data

# Generate figure
plt.figure(figsize=(7, 10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=0,
                                   standard_parallels=(45, 89))
ax = plt.axes(projection=projection, frameon=False)
ax.set_extent((0, 359, 0, 90), crs=ccrs.PlateCarree())
ax.coastlines(linewidth=0.5)

# Plot data and create colorbar
newcmp = gvcmaps.BlWhRe

wind = V.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(),
                       add_colorbar=False, levels=24)
plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True,
             ticks=np.arange(-48, 48, 8), pad=0.1, aspect=12)
plt.title(V.long_name, loc='left', size=16)
plt.title(V.units, loc='right', size=16)
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

# Generate figure
plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
projection = ccrs.LambertConformal(central_longitude=-25, cutoff=20,
                                   standard_parallels=(45, 89))
ax = plt.axes(projection=projection)
ax.set_global()
ax.coastlines(linewidth=0.5)


# Create a custom boundary to achive the wedge shape
wedge = wedge_path(118, 240, 0.5, center=(0.5, 0.5), width=0.425)
ax.set_boundary(wedge, transform=ax.transAxes)

# Plot data and create colorbar
newcmp = gvcmaps.BlWhRe

wind = masked.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(),
                            add_colorbar=False, levels=24)
plt.colorbar(wind, ax=ax, orientation='horizontal', drawedges=True,
             ticks=np.arange(-48, 48, 8), pad=0.1, aspect=12)
plt.title(masked.long_name, loc='left', size=16)
plt.title(masked.units, loc='right', size=16)

plt.show()
