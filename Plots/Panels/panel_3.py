"""
panel_3.py
===============
Two panel image with shared colorbar and title

NCL docs: https://www.ncl.ucar.edu/Applications/panel.shtml

NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_3.ncl

NCL output: https://www.ncl.ucar.edu/Applications/Images/panel_3_lg.png
"""

###############################################################################
# Concepts illustrated:
#   - Paneling plots vertically on a page ``plt.subplots``
#   - Adding a common title to paneled plots ``matplotlib.Figure.suptitle``
#   - Adding a common labelbar (or colorbar) to paneled plots ``matplotlib.Figure.colorbar``
#   - Subsetting a color map

###############################################################################
# Lets read the netCDF dataset using xarray and choose the second timestamp.
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import geocat.datafiles

ds = xr.open_dataset(geocat.datafiles.get("netcdf_files/uv300.nc")).isel(time=1)

###############################################################################
# Now we will define a few utility functions.
# The plot requires filled colored contours, with black labelled contours, so we'll
# make utility function that does all that.
#
# We will then call this function twice, once with `ds.U` and then with `ds.V`

levels = np.arange(-10, 46, 5)


###############################################################################
# The NCL example uses a truncated colormap. Here's a small function that does that


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """
    Utility function that truncates a colormap. Copied from  https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """

    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        name="trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        colors=cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


###############################################################################
# This is the main plotting function. We do this so as not to repeat many lines of code since we
# need to make the same figure with two different variables.


def plot_labelled_filled_contours(data, ax=None):
    """
    A utility function for convenience that plots labelled, filled contours with black contours
    marking each level.It will return a dictionary containing three objects corresponding to the
    filled contours, the black contours, and the contour labels.
    """

    cmap = truncate_colormap(mpl.cm.rainbow, 0.2, 0.9)

    handles = dict()
    handles["filled"] = data.plot.contourf(
        ax=ax,  # this is the axes we want to plot to
        cmap=cmap,  # our special colormap
        levels=levels,  # contour levels specified outside this function
        xticks=np.arange(-180, 181, 30),  # nice x ticks
        yticks=np.arange(-90, 91, 30),  # nice y ticks
        transform=ccrs.PlateCarree(),  # data projection
        add_colorbar=False,  # don't add individual colorbars for each plot call
        add_labels=False,  # turn off xarray's automatic Lat, lon labels
    )

    # matplotlib's contourf doesn't let you specify the "edgecolors" (MATLAB terminology)
    # instead we plot black contours on top of the filled contours
    handles["contour"] = data.plot.contour(
        ax=ax,
        levels=levels,
        colors="k",  # note plurals in this and following kwargs
        linestyles="-",
        linewidths=0.5,
        add_labels=False,  # again turn off automatic labels
    )

    # Label the contours
    ax.clabel(
        handles["contour"], fontsize="small", fmt="%.0f",  # Turn off decimal points
    )

    # make a nice title
    title = f"{data.attrs['long_name']} [{data.attrs['units']}]"
    ax.set_title(title, loc="left", y=1.05)

    return handles


###############################################################################
# Here's how this function works

ax = plt.gca(projection=ccrs.PlateCarree())
plot_labelled_filled_contours(ds.U, ax)

###############################################################################
# These next two functions add nice axes decorations and make the plot look more
# like NCL


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


###############################################################################
# Now we'll make two panels (subplots in matplotlib terminology) using ``plt.subplots``
# We'll specify ``constrained_layout=True`` which will attempt to automatically
# layout panels, colorbars and axes decorations nicely.
# https://matplotlib.org/tutorials/intermediate/constrainedlayout_guide.html

f, ax = plt.subplots(
    2,  # 2 rows
    1,  # 1 column
    constrained_layout=True,  # "magic"
    subplot_kw={"projection": ccrs.PlateCarree()},  # specify plot projection
)

# first U, save handles so that we can make a nice colorbar later
handles = plot_labelled_filled_contours(ds.U, ax=ax[0])

# Now V
plot_labelled_filled_contours(ds.V, ax=ax[1])

cbar = f.colorbar(
    handles["filled"],  # make colorbar appropriate for this object
    ax=ax,  # a list of *two* axes, matplotlib will steal space from both these to fit the colorbar
    orientation="horizontal",  # horizontal colorbars are on the bottom by default
    aspect=30,  # aspect ratio of colorbar, just because we can.
)
cbar.set_ticks(levels)  # set the tick labels on the colorbar

# make axes look nice and add coastlines
[nclize_axis(axes) for axes in ax.flat]
[add_lat_lon_ticklabels(axes) for axes in ax.flat]
[axes.coastlines(linewidth=0.5) for axes in ax.flat]

# nice figure size in inches
f.set_size_inches((6, 7))

# a common title
f.suptitle("A plot with a common label bar (colorbar)")

# show the plot!
plt.show()
