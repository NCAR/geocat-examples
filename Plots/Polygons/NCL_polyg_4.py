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
import geocat.viz as gcv

ds = xr.open_dataset("../../data/netcdf_files/uv300.nc").isel(time=1)

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

# Specify contour levels (from -12 to 40 by 4).   The top range value of 44 is not included in the levels.
levels = np.arange(-12, 44, 4)

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

gcv.util.nclize_axis(ax)
gcv.util.add_lat_lon_ticklabels(ax)

plt.show()
