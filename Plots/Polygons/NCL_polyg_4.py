"""
NCL_polyg_4.py
==============
 Concepts illustrated:
   - Drawing a cylindrical equidistant map
   - Zooming in on a particular area on a cylindrical equidistant map
   - Attaching an outlined box to a map plot
   - Attaching filled polygons to a map plot
   - Filling in polygons with a shaded pattern
   - Changing the color and thickness of polylines
   - Changing the color of a filled polygon
   - Labeling the lines in a polyline
   - Changing the density of a fill pattern
   - Adding text to a plot

This Python script reproduces the NCL plot script found here: https://www.ncl.ucar.edu/Applications/Scripts/polyg_4.ncl
"""

###############################################################################
# Import the necessary python libraries
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


ds = xr.open_dataset("../../data/netcdf_files/uv300.nc").isel(time=1)

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
# Another text/markdown cell

def xr_add_cyclic(da, coord):
    from cartopy.util import add_cyclic_point

    cyclic_data, cyclic_coord = cartopy.util.add_cyclic_point(da.values, coord=da[coord])

    coords = da.coords.to_dataset()
    coords[coord] = cyclic_coord
    return xr.DataArray(cyclic_data, dims=da.dims, coords=coords.coords)



###############################################################################
# Note the inline comment in the previous code cell. This was not converted to
# its own markdown cell because it was not contiguously preceeded with a
# comment line beginning with 20+ '#' characters.

# first add continents
continents = cartopy.feature.NaturalEarthFeature(
    name="coastline",
    category="physical",
    scale="50m",
    edgecolor="None",
    facecolor="lightgray",
)

#$map_extent = [-130, 0, -8, 25]
map_extent = [-130, 0, -20, 40]
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(continents)
ax.set_extent(map_extent, crs=ccrs.PlateCarree())


levels = np.arange(-12, 40, 4)
# Using a dictionary makes it easy to reuse the same keyword arguments twice for the contours
kwargs = dict(
    levels=levels,  # contour levels specified outside this function
    xticks=[-120, -90, -60, -30, 0],  # nice x ticks
    yticks=[-20, 0, 20, 40],  # nice y ticks
    transform=ccrs.PlateCarree(),  # ds projection
    add_colorbar=False,  # don't add individual colorbars for each plot call
    add_labels=False,  # turn off xarray's automatic Lat, lon labels
    colors="k",  # note plurals in this and following kwargs
    linestyles="-",
    linewidths=0.5,
)

# Create contour plot
hdl = ds.U.plot.contour(
    x="lon",  # not strictly necessary but good to be explicit
    y="lat",
    ax=ax,  # this is the axes object we want to plot to
    **kwargs,
)

# Add contour labels
ax.clabel(hdl,
          np.arange(-8, 32, 8),  # only label these contour levels
          fontsize="small",
          fmt="%.0f")  # Turn off decimal points

# Create square polygon
x_points = [-90.0, -45.0,-45.0, -90.0,-90.0]
y_points = [30.0,  30.0,  0.0,   0.0, 30.0]

# Plot the hatch pattern first
ax.fill(x_points, y_points,
        edgecolor='purple',      # Box hatch fill is purple
        zorder=5,             # Place on top of map
        fill=False,
        hatch='...',
        linewidth=0.5
        )

# Plot the box on top, because the color is different.
ax.fill(x_points, y_points,
        edgecolor='red',      # Box edge is red
        zorder=6,             # Place on top of hatch
        fill=False,
        )


nclize_axis(ax)
add_lat_lon_ticklabels(ax)

plt.show()