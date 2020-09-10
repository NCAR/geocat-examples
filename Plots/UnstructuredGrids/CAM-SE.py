"""
CAM-SE.py
===============
This script illustrates the following concepts:
    - Plotting variables on a CAM-SE "cube-sphere" grid.


Note:
    - See http://www.cesm.ucar.edu/models/cesm2/atmosphere/ for an overview of CAM
    - See https://www.earthsystemcog.org/projects/dcmip-2016/HOMME-NH for description on CAM-SE grid
    - The data set in this example does not provide explicit connectivity information. Hence, 
      a triangle mesh is constructed via Delauny triangulation, which may not be ideal (it's time
      consuming and will introduce errors that my or may not be signficant for plotting purposes).
    - Need an example with explicit connectivity information.
    - Need to check performance with high resolution, adaptive-refinement data set. 
    - Need an example with region subsetting (i.e. extracting a retangular lat-lon region)
    - Several CAM-SE data sets are available in
      /glade/p/cisl/vast/vapor/data/Source/CAM/NotSupported/CAM-SE. They are all too
    - large for GitHub and would need to be reduced by removing variables with NCO

"""

###############################################################################
# Import packages:
import xarray as xr
import matplotlib
import cartopy.crs as ccrs

import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np
import math as math

###############################################################################
# Make triangle boundary mask:
#
# Create a boolean mask of valid triangles. The mask will be false wherever
# the distance between two triangle vertices is greater than 't'. We are essentially
# masking off triangles that have vertices on both sides of the longitudinal cut line
# where we split the periodic domain.
#
def makeBoundaryMask(lons,tris,t):
    return  (np.abs(lons[tris[:,0]]-lons[tris[:,1]]) < t) & (np.abs(lons[tris[:,0]]-lons[tris[:,2]]) < t)


###############################################################################
# Read data:
#
#
datafile  = '//Users/clyne/Data/CAM/CAM-SE/f.asd2017.cesm20b05.FAMIPC6CLM5.ne0conus30x8_t12.cam.i.1980-01-01-00000.nc'
ds = xr.open_dataset(datafile, decode_times=False)

# Is this  needed?
#
ds.set_coords(('lat', 'lon'))

var = ds.T.isel(time=0, lev=0).values
x = ds.lon.values
y = ds.lat.values

projection = ccrs.PlateCarree(central_longitude=180.0)
x, y, _ = projection.transform_points(ccrs.PlateCarree(), x, y).T

###############################################################################
# Triangulate cube-sphere mesh:
# 
# Triangulate the grid nodes. Because no explicit node connectivity information is provided
# in this data set we use Delauny triangulation to synthesize a mesh that can be plotted by
# MPL
triangles = Triangulation(x, y)

plt.figure(figsize=(12, 7.2))

# Generate axes using Cartopy projection
ax = plt.axes(projection=projection)


# Use global map and draw coastlines
ax.set_global()
ax.coastlines(linewidth=1.0, resolution="110m")
ax.set_aspect('equal')

ax.tripcolor(triangles,var,cmap='coolwarm' )
ax.set_title('CAM-SE plotted without explicit mesh connectivity')
plt.show()

