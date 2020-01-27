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

#
#
#
# ###############################################################################
# # Another text/markdown cell
#
# def xr_add_cyclic(da, coord):
#     from cartopy.util import add_cyclic_point
#
#     cyclic_data, cyclic_coord = cartopy.util.add_cyclic_point(da.values, coord=da[coord])
#
#     coords = da.coords.to_dataset()
#     coords[coord] = cyclic_coord
#     return xr.DataArray(cyclic_data, dims=da.dims, coords=coords.coords)



###############################################################################
# Draw the basic contour plot

# first add continents
continents = cartopy.feature.NaturalEarthFeature(
    name="coastline",
    category="physical",
    scale="50m",
    edgecolor="None",
    facecolor="lightgray",
)

map_extent = [-130, 0, -20, 40]
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(continents)
ax.set_extent(map_extent, crs=ccrs.PlateCarree())


levels = np.arange(-12, 40, 4)
# Using a dictionary prevents repeating the same keyword arguments twice for the contours.
kwargs = dict(
    levels=levels,  # contour levels specified outside this function
    xticks=[-120, -90, -60, -30, 0],  # nice x ticks
    yticks=[-20, 0, 20, 40],  # nice y ticks
    transform=ccrs.PlateCarree(),  # ds projection
    add_colorbar=False,  # don't add individual colorbars for each plot call
    add_labels=False,  # turn off xarray's automatic Lat, lon labels
    colors="gray",  # note plurals in this and following kwargs
    linestyles="-",
    linewidths=0.5,
)

# Create contour plot
hdl = ds.U.plot.contour(
    x="lon",  # not strictly necessary but good to be explicit
    y="lat",
    ax=ax,    # this is the axes object we want to plot to
    **kwargs,
)

# Add contour labels.   Default contour labels are sparsely placed, so we specify label locations manually.
# Label locations only need to be approximate; the nearest contour will be selected.
label_locations = [(-123, 35), (-116, 17), (-94, 4), (-85, -6), (-95, -10),
                   (-85, -15), (-70, 35), (-42, 28), (-54, 7), (-53, -5),
                   (-39, -11), (-28, 11), (-16, -1), (-8, -9),             # Python allows trailing list separators.
                   ]
ax.clabel(hdl,
          np.arange(-8, 24, 8),    # Only label these contour levels: [-8, 0, 8, 16]
          fontsize="small",
          colors="black",
          fmt="%.0f",              # Turn off decimal points
          manual=label_locations,  # Manual label locations
          inline=False)            # Don't remove the contour line where labels are located.

###############################################################################
# Create a rectangular polygon with hatch pattern.

x_points = [-90.0, -45.0, -45.0, -90.0, -90.0]
y_points = [ 30.0,  30.0,   0.0,   0.0,  30.0]

# Plot the hatch pattern first
ax.fill(x_points, y_points,
        edgecolor='purple',   # Box hatch pattern is purple.
        zorder=2,             # Place on top of map (larger zorder is closer to viewer).
        fill=False,
        hatch='...',          # Adding more or fewer dots to '...' will change hatch density.
        linewidth=0.5,        # Make each dot smaller
        alpha=0.2             # Make hatch semi-transparent using alpha level in range [0, 1].
        )


# Create a rectangle patch, to color the border of the rectangle a different color.
# Specify the rectangle as a corner point with width and height, to help place text more easily.
left, width = -90, 45
bottom, height = 0, 30
right = left + width
top = bottom + height

p = plt.Rectangle((left, bottom), width, height, fill=False,
                  zorder=3,          # Plot on top of the purple box border.
                  edgecolor='red',
                  alpha=0.5)         # Lower color intensity.
ax.add_patch(p)

###############################################################################
# Draw text labels around the box.

# Change the default padding around a text box to zero, making it a "tight" box.
# Create "text_args" to keep from repeating code when drawing text.
text_shared_args = dict(
    fontsize=8,
    bbox=dict(boxstyle='square, pad=0', fc='white', ec='white'),
)

# Draw top text
ax.text(left + 0.6 * width, top, 'test',
        horizontalalignment='right',
        verticalalignment='center',
        **text_shared_args
        )

# Draw bottom text.   Change text background to match the map.
ax.text(left + 0.5 * width, bottom, 'test',
        horizontalalignment='right',
        verticalalignment='center',
        fontsize=8,
        bbox=dict(boxstyle='square, pad=0', fc='lightgrey', ec='lightgrey'),
        )

# Draw left text
ax.text(left, top, 'test',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=90,
        **text_shared_args
        )

# Draw right text
ax.text(right, bottom, 'test',
        horizontalalignment='center',
        verticalalignment='bottom',
        rotation=-90,
        **text_shared_args
        )


###############################################################################
# Now draw some triangles with various hatch patterns.


# Define a utility function that draws a polygon and then erases its border with another polygon.

def draw_hatch_polygon(xvals, yvals, hatchcolor, hatchpattern):
    """ Draw a polygon filled with a hatch pattern, but with no edges on the polygon.
    """
    ax.fill(xvals, yvals,
            edgecolor=hatchcolor,   # Box hatch fill is brown.
            zorder=0,               # Place on top of map (larger zorder is closer to viewer).
            fill=False,
            linewidth=0.5,
            hatch=hatchpattern,
            alpha=0.3
            )

    # Hatch color and polygon edge color are tied together, so we have to draw a white polygon edge
    # on top of the original polygon to remove the edge.
    ax.fill(xvals, yvals,
            edgecolor='white',   # Box hatch fill is brown.
            zorder=0,            # Place on top of map (larger zorder is closer to viewer).
            fill=False,
            linewidth=0.5
            )

x_tri = np.array([-125, -115, -120])
y_tri = [-15,   -10,    5]

draw_hatch_polygon(x_tri, y_tri, 'brown', 'xxxx')

draw_hatch_polygon(x_tri + 10, y_tri, 'blue', 'xxx')

draw_hatch_polygon(x_tri + 20, y_tri, 'forestgreen', 'xx')

###############################################################################
# Add title and tick marks to match NCL conventions.

# Draw left and right title text
ax.text(0.0, 1.05, "Zonal Wind", fontsize=12, transform=ax.transAxes)
ax.text(1.0, 1.05, "m/s", fontsize=12, horizontalalignment='right', transform=ax.transAxes)

nclize_axis(ax)
add_lat_lon_ticklabels(ax)

plt.show()