"""
mask_1.py
===============
Demonstrates the use of the xarray's where function and 
a masking array to mask out land or ocean.

- Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/mask_1.ncl
- https://www.ncl.ucar.edu/Applications/Images/mask_1_1_lg.png
- https://www.ncl.ucar.edu/Applications/Images/mask_1_2_lg.png
"""

import cartopy.crs as ccrs
import cmaps
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles

###############################################################################
# Read in the netCDF file
# =======================

ds = (
    xr.open_dataset(
        geocat.datafiles.get("netcdf_files/atmos.nc"), decode_times=False
    )  # Disable time decoding due to missing necessary metadata
    .isel(time=0)
    .drop("time")
)


###############################################################################
# Data Masking
# =============


def xr_add_cyclic(da, coord):
    """
    Function to add a cyclic point to an array and a 
    corresponding coordinate.
    """
    from cartopy.util import add_cyclic_point

    cyclic_data, cyclic_coord = add_cyclic_point(da.values, coord=da[coord])

    coords = da.coords.to_dataset()
    coords[coord] = cyclic_coord
    return xr.DataArray(
        cyclic_data,
        dims=da.dims,
        coords=coords.coords,
        attrs=da.attrs,
        encoding=da.encoding,
    )


# Use xarray's where function to mask out land and then ocean data

land_only = ds.TS.where(ds.ORO == 1.0)
ocean_only = ds.TS.where(ds.ORO == 0.0)
land_only = xr_add_cyclic(land_only, "lon")
ocean_only = xr_add_cyclic(ocean_only, "lon")


###############################################################################
# Define a few utility functions
# ==============================


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Utility function that truncates a colormap. This is useful when 
    the user wants to construct a "custom" colormap by using a segment 
    of a preset colormap.  
    
    Copied from  https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """

    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def add_lat_lon_ticklabels(ax):
    """
    Nice latitude, longitude tick labels
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(
        zero_direction_label=False, dateline_direction_label=False
    )
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


def nclize_axis(ax):
    """
    Utility function to make plots look like NCL plots
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=1.5,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=5,
        width=0.75,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )


def plot_filled_contours(data, vmin, vmax, ax=None, cmap="viridis"):
    """
    A utility function for convenience that plots labelled, filled contours.
    """

    filled = data.plot.contourf(
        ax=ax,  # this is the axes we want to plot to
        cmap=cmap,  # our special colormap
        levels=levels,  # contour levels specified outside this function
        xticks=np.arange(-180, 181, 30),  # nice x ticks
        yticks=np.arange(-90, 91, 30),  # nice y ticks
        transform=ccrs.PlateCarree(),  # data projection
        add_colorbar=False,  # don't add individual colorbars for each plot call
        add_labels=False,  # turn off xarray's automatic Lat, lon labels
        vmin=vmin,
        vmax=vmax,
    )

    # make a nice title
    ax.set_title(f"{data.attrs['long_name']}", loc="left", y=1.05)
    ax.set_title(f"{data.attrs['units']}", loc="right", y=1.05)

    return filled


###############################################################################
# Plot Ocean Only
# ===============

levels = np.arange(260, 305, 2)
plt.register_cmap("BlAqGrYeOrRe", truncate_colormap(cmaps.BlAqGrYeOrRe, 0.1, 1.0))
cmap = plt.cm.get_cmap("BlAqGrYeOrRe", 22)

f, ax = plt.subplots(1, 1, subplot_kw={"projection": ccrs.PlateCarree()})
filled = plot_filled_contours(ocean_only, vmin=260, vmax=304, ax=ax, cmap=cmap)

cbar = f.colorbar(
    filled,  # make colorbar appropriate for this object
    ax=ax,  # a list of *two* axes, matplotlib will steal space from both these to fit the colorbar
    orientation="horizontal",  # horizontal colorbars are on the bottom by default
    aspect=30,  # aspect ratio of colorbar, just because we can.
    drawedges=True,
)


cbar.set_ticks(np.arange(262, 304, 4))
# make axes look nice and add coastlines
nclize_axis(ax)
add_lat_lon_ticklabels(ax)
ax.coastlines(linewidth=0.5, resolution="110m")

# nice figure size in inches
f.set_size_inches((10, 6))


# a common title
f.suptitle("Ocean Only", fontsize=24, fontweight="bold")
plt.show()

###############################################################################
# Plot Land Only
# ===============

levels = np.arange(215, 316, 4)
plt.register_cmap("BlAqGrYeOrRe", truncate_colormap(cmaps.BlAqGrYeOrRe, 0.1, 1.0))
cmap = plt.cm.get_cmap("BlAqGrYeOrRe", 32)

f, ax = plt.subplots(1, 1, subplot_kw={"projection": ccrs.PlateCarree()})
filled = plot_filled_contours(land_only, vmin=215, vmax=315, ax=ax, cmap=cmap)

cbar = f.colorbar(
    filled,  # make colorbar appropriate for this object
    ax=ax,  # a list of *two* axes, matplotlib will steal space from both these to fit the colorbar
    orientation="horizontal",  # horizontal colorbars are on the bottom by default
    aspect=30,  # aspect ratio of colorbar, just because we can.
    drawedges=True,
)


cbar.set_ticks(np.arange(219, 304, 12))
# make axes look nice and add coastlines
nclize_axis(ax)
add_lat_lon_ticklabels(ax)
ax.coastlines(linewidth=0.5, resolution="110m")

# nice figure size in inches
f.set_size_inches((10, 6))

# a common title
f.suptitle("Land Only", fontsize=24, fontweight="bold")
plt.show()
