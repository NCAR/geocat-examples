"""
issue272_case2i.py
===============
This script illustrates the following concepts:
    - Exploring the Datashader capabilities and parallel rendering performance on an
    unstructured grid case (Case 2.ii. at issue https://github.com/NCAR/GeoCAT-examples/issues/272).
    - Generating a synthetic mesh (rectangular) with no connectivity data. i.e. all we really
    have are a collection of points.
    - Triangulating the rectangular mesh to generate a triangle mesh. Currently Matplotlib's
    Delaunay triangulation is used for this. It's time consuming and will introduce errors
    that may or may not be significant for plotting purposes. Any alternative solution from
    Datashader stack for this?
    - Rendering the triangle mesh. Currently Matplotlib's "tripcolor" function is used for
    this. Any alternative solution from Datashader and Geoviews stack for this?

"""

###############################################################################
# Import packages:
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import time


###############################################################################
# User-defined arguments
num_pts = 1740980    # Number of points can be adjusted to analyze algorithm performance


###############################################################################
# Generate a synthetic rectangular mesh:

# Generate lon and lat values
x = np.random.uniform(low=0, high=360, size=(num_pts,))
y = np.random.uniform(low=-90, high=90, size=(num_pts,))

# Generate random (meaningless but ok) values for points
var = np.random.uniform(low=183, high=262, size=(num_pts,))

# Use PlateCarree projection
projection = ccrs.PlateCarree(central_longitude=180.0)
x, y, _ = projection.transform_points(ccrs.PlateCarree(), x, y).T


###############################################################################
# Triangulate cube-sphere mesh:

# Profile execution time of triangulation, set start time
t0 = time.time()

# Triangulate the grid nodes using matplotlib.tri.Triangulation(). Because no explicit node
# connectivity information is provided in this data set we use Delaunay triangulation to
# synthesize a mesh that can be plotted by MPL
triangles = Triangulation(x, y)

# Profile execution time of triangulation, set end time and print duration
t1 = time.time()
print("Triangulation takes: ", t1 - t0, "seconds")


###############################################################################
# Render:

plt.figure(figsize=(12, 7.2))

# Generate axes using Cartopy projection
ax = plt.axes(projection=projection)

# Use global map and draw coastlines
ax.set_global()
ax.coastlines(linewidth=1.0, resolution="110m")
ax.set_aspect('equal')

# Profile execution time of rendering, set start time
t0 = time.time()

# Render the triangles using matplotlib.pyplot.tripcolor().
ax.tripcolor(triangles,var,cmap='coolwarm' )

# Profile execution time of rendering, set end time and print duration
t1 = time.time()
print("Rendering of the triangles takes: ", t1 - t0, "seconds")

# Set a title and show the plot
ax.set_title('Triangulated mesh plotted without explicit mesh connectivity')
plt.show()

