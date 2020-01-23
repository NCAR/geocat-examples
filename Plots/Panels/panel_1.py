"""
panel_1.py
===============
Three panel image with shared colorbar and title


NCL docs: https://www.ncl.ucar.edu/Applications/panel.shtml

NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_1.ncl

NCL output: https://www.ncl.ucar.edu/Applications/Images/panel_1_lg.png

"""

###############################################################################
# Concepts illustrated:
#   - Paneling plots vertically on a page ``plt.subplots``
#   - Adding a common title to paneled plots ``matplotlib.Figure.suptitle``
#   - Adding a common labelbar (or colorbar) to paneled plots ``matplotlib.Figure.colorbar``
#   - Subsetting a color map

###############################################################################
# Lets read the netCDF dataset using xarray and choose the second timestamp.
import cartopy
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

ds = xr.open_dataset("../../data/netcdf_files/uv300.nc").isel(time=1)

###############################################################################
# These next two functions add nice axes decorations and make the plot look more
# like NCL


def add_lat_lon_ticklabels(ax):
    """
    Nice latitude, longitude tick labels
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
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


###############################################################################
# Now we'll make three panels (subplots in matplotlib terminology) using ``plt.subplots``
# We'll specify ``constrained_layout=True`` which will attempt to automatically
# layout panels, colorbars and axes decorations nicely.
# https://matplotlib.org/tutorials/intermediate/constrainedlayout_guide.html

f, ax = plt.subplots(
    3,  # 3 rows
    1,  # 1 column
    constrained_layout=True,  # "magic"
    subplot_kw={"projection": ccrs.PlateCarree()},  # specify plot projection
)


# first add continents
continents = cartopy.feature.NaturalEarthFeature(
    name="coastline",
    category="physical",
    scale="50m",
    edgecolor="None",
    facecolor="lightgray",
)
[axes.add_feature(continents) for axes in ax.flat]



levels = np.arange(-48, 48, 4)

# Using a dictionary makes it easy to reuse the same keyword arguments twice for the contours
kwargs = dict(
    levels=levels,  # contour levels specified outside this function
    xticks=np.arange(-180, 181, 30),  # nice x ticks
    yticks=np.arange(-90, 91, 30),  # nice y ticks
    transform=ccrs.PlateCarree(),  # ds projection
    add_colorbar=False,  # don't add individual colorbars for each plot call
    add_labels=False,  # turn off xarray's automatic Lat, lon labels
    colors="k",  # note plurals in this and following kwargs
    linestyles="-",
    linewidths=0.5,
)


# first U
hdl = ds.U.plot.contour(
    x="lon",  # not strictly necessary but good to be explicit
    y="lat",
    ax=ax[0],  # this is the axes we want to plot to
    **kwargs,
)
# Label the contours
ax[0].clabel(
    hdl,
    np.arange(0, 32, 8),  # only label these contour levels
    fontsize="small",
    fmt="%.0f",  # Turn off decimal points
)
ax[0].set_title("Zonal Wind [m/s]", loc="left")

# now for V
hdl = ds.V.plot.contour(x="lon", y="lat", ax=ax[1], **kwargs,)
ax[1].clabel(
    hdl,
    [0],  # only label these contour levels
    fontsize="small",
    fmt="%.0f",  # Turn off decimal points
)
ax[1].set_title("Meridional Wind [m/s]", loc="left")

# now draw arrows
# xarray doesn't have a quiver method (yet)
# the NCL code plots every 4th value in lat, lon
# this is the equivalent of u(::4, ::4)
subset = ds.isel(lat=slice(None, None, 4), lon=slice(None, None, 4))
ax[2].quiver(
    subset.lon,
    subset.lat,
    subset.U,
    subset.V,
    width=0.0015,  # thinner than default
    transform=ccrs.PlateCarree(),
    zorder=2, # hack to make sure quiver plots on top of continents
    scale=1100,  # adjust till it looks right
)
ax[2].set_title("Vector Wind", loc="left")

# cartopy axes require this to be manual
ax[2].set_xticks(kwargs["xticks"])
ax[2].set_yticks(kwargs["yticks"])

# make axes look nice and add coastlines
[nclize_axis(axes) for axes in ax.flat]
[add_lat_lon_ticklabels(axes) for axes in ax.flat]

# nice figure size in inches
f.set_size_inches((5, 8))
