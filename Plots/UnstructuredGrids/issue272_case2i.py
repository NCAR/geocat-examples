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

from PIL import Image
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from scipy.spatial import Delaunay
import sys

# HoloViz packages:
import holoviews as hv, datashader as ds
import holoviews.operation.datashader as hds 
import geoviews.feature as gf # only needed for coastlines
hv.extension("matplotlib")
plt.switch_backend('agg')

###############################################################################
# Define timer

import time
class Timer:
    """Context manager for measuring execution times"""
    def __init__( self, label=""): self.label = label
    def __enter__(self):self.t0 = time.time() ; return self
    def __exit__( self, exc_type, exc_value, exc_tb):
        t1 = time.time()
        print(self.label, "takes:", t1 - self.t0, "seconds")


###############################################################################
# suppress warnings triggered by cartopy 0.18
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


###############################################################################
# User-defined arguments:

# Lon-lat resolutions in degrees
# NOTE: Single-threaded matplotlib implementation in this script was first
# examined on a 3-km lon-lat resolution (i.e. 0.03 degrees) case and ran for
# more than 7 hours with close-to-full memory use on a 16 GB memory system
# but did not seem to succeed it (No further analysis or profiling done though).
# However, below 10 km resolution case succeeds, taking 145 seconds for triangulation
# and 99 seconds for rendering.

factor = 200 # Use factor=1 for roughly 10 km around equator; factor=200 for quick test
if len(sys.argv)>1:
   factor = float(sys.argv[1])

lat_res = 0.1*factor
lon_res = 0.1*factor

# Lon-lat min, max
lon_min = 0
lon_max = 360
lat_min = -90
lat_max = 90


###############################################################################
# Generate a synthetic rectangular mesh:

# Generate lon-lat value vectors first
lons = np.arange(lon_min, lon_max, lon_res) # jbednar: these don't actually include lon_max or lat_max; use np.linspace()?
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

# Triangulate the grid nodes using matplotlib.tri.Triangulation(). Because no explicit node
# connectivity information is provided in this data set we use Delaunay triangulation to
# synthesize a mesh that can be plotted by MPL
with Timer("MPL Triangulation"):
    triangles = Triangulation(x, y)

with Timer("SciPy Triangulation"):
    points = np.stack([x,y,var]).T
    tri = Delaunay(points[:,0:2])

###############################################################################
# Render with Datashader+HoloViews+Matplotlib:
filepath = '/tmp/output_ds.png'

# First rendering forces JIT compilation so is always slower
with Timer("Datashader-based rendering 1"):
    nodes = hv.Points(points, vdims='z')
    trimesh = hv.TriMesh((tri.simplices, nodes)).opts(filled=True, edge_color='z')
    img = hds.rasterize(trimesh, aggregator=ds.mean('z'), interpolation=None, dynamic=False)
    out = (img.opts(cmap="coolwarm", fig_inches=10) * gf.coastline(projection=projection)).opts(fig_size=330)
    hv.save(out, filepath, fmt='png', dpi=144)

# Second rendering should be what characterizes interactive use
with Timer("Datashader-based rendering 2"):
    nodes = hv.Points(points, vdims='z')
    trimesh = hv.TriMesh((tri.simplices, nodes)).opts(filled=True, edge_color='z')
    img = hds.rasterize(trimesh, aggregator=ds.mean('z'), interpolation=None, dynamic=False)
    out = (img.opts(cmap="coolwarm", fig_inches=10) * gf.coastline(projection=projection)).opts(fig_size=330)
    hv.save(out, filepath, fmt='png', dpi=144)

###############################################################################
# Render with Matplotlib:
filepath = '/tmp/output_mpl.png'

with Timer("Matplotlib-based rendering"):
    plt.figure(figsize=(12, 7.2))
    
    # Generate axes using Cartopy projection
    ax = plt.axes(projection=projection)
    
    # Use global map and draw coastlines
    ax.set_global()
    ax.coastlines(linewidth=1.0, resolution="110m")
    ax.set_aspect('equal')
    
    # Render the triangles using matplotlib.pyplot.tripcolor().
    ax.tripcolor(triangles,var,cmap='coolwarm' )
    
    # Set a title and export the plot
    ax.set_title('Triangulated mesh plotted without explicit mesh connectivity')
    plt.savefig(filepath, dpi=144)




