"""
issue272_case2i.py
===============
This script illustrates the following concepts:
    -            Exploring the Datashader capabilities and parallel rendering performance on an unstructured grid case (Case 2.ii. at issue https://github.com/NCAR/GeoCAT-examples/issues/272).
    - Generating a synthetic mesh (rectangular) with no connectivity data. i.e. all we really have are a collection of points.
    - Triangulating the rectangular mesh to generate a triangle mesh. Currently Matplotlib's Delaunay triangulation is used for this. It's time consuming and will introduce errors that may or may not be significant for plotting purposes. Any alternative solution from Datashader stack for this?
    - Rendering the triangle mesh. Currently Matplotlib's "tripcolor" function is used for this. Any alternative solution from Datashader and Geoviews stack for this?
    - Profiling the execution time of triangulation and rendering seperately

"""

###############################################################################
# Import packages:

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import time


###############################################################################
# User-defined arguments:

# Lon-lat resolutions in degrees
# NOTE: Single-threaded matplotlib implementation in this script was first
# examined on a 3-km lon-lat resolution (i.e. 0.03 degrees) case and ran for
# more than 7 hours with close-to-full memory use on a 16 GB memory system
# but did not seem to succeed it (No further analysis or profiling done though).
# However, below 10 km resolution case succeeds, taking 145 seconds for triangulation
# and 99 seconds for rendering.
lon_res = 0.1     # Roughly 10 km around equator
lat_res = 0.1

# Lon-lat min, max
lon_min = 0
lon_max = 360
lat_min = -90
lat_max = 90


###############################################################################
# Generate a synthetic rectangular mesh:

# Generate lon-lat value vectors first
lons = np.arange(lon_min, lon_max, lon_res)
lats = np.arange(lat_min, lat_max, lat_res)


# Generate lon-lat meshgrid
x, y = np.meshgrid(lons, lats)

# Convert x and y meshes to vectors
num_pts = x.size
x = x.reshape(num_pts, )
y = y.reshape(num_pts, )

# Generate random (meaningless but ok) values for the points
# Low and high values below are from a CAM-SE data, which is meaningless here,
# but no problem
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

