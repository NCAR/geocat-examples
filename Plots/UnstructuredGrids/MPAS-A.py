"""
MPAS-A.py
===============
This script illustrates the following concepts:
    - Plotting variables on the MPAS-A primary mesh
    - Plotting variables on the MPAS-A dual mesh


Note:
    - See https://mpas-dev.github.io/ for info on  MPAS and MPAS-A
    - See https://github.com/MPAS-Dev/MPAS-Tools/pull/319 for another approach to this problem 
    - There are also "edge" variables defined on the MPAS grid. This script does not show 
      how to plot them.
    - The performance of this script on larger data (e.g. ~2km grid) is not known and 
      may be problematic
    - Need an example with region subsetting (i.e. extracting a retangular lat-lon region)
    - A copy of this public data set is available on glade in 
      /glade/p/cisl/vast/vapor/data/Source/MPAS/MPAS_V4.0. It is too large for GitHub, but
      could be reduced in size by removing variables with NCO.

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
# Range restrict:
#
# Restrict range of longitude values to ensure that max(lon)-min(lon) <= 360.0. This
# may be a no-op in most cases.
#
def rangeRestrict(lons):
    m = np.amin(lons)
    while np.any(lons > (m+360.0)):
        lons = np.where(lons > (m+360.0), lons-360.0, lons)
    return(lons)




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
# Triangulate MPAS primary mesh:
#
# Triangulate each polygon in a heterogenous mesh of n-gons by connecting
# each internal polygon vertex to the first vertex. Uses the MPAS
# auxilliary variables verticesOnCell, and nEdgesOnCell
#
def triangulatePoly(verticesOnCell, nEdgesOnCell):
    
    # Calculate the number triangles. nEdgesOnCell gives the number of vertices for each cell (polygon)
    # The number of triangles per polygon is the number of vertices minus 2.
    #
    nTriangles = np.sum(nEdgesOnCell - 2)
    
    triangles = np.ones((nTriangles, 3), dtype=np.int64)
    nCells = verticesOnCell.shape[0]
    triIndex = 0
    for j in range(nCells):
        for i in range(nEdgesOnCell[j]-2):
            triangles[triIndex][0] = verticesOnCell[j][0]
            triangles[triIndex][1] = verticesOnCell[j][i+1]
            triangles[triIndex][2] = verticesOnCell[j][i+2]
            triIndex += 1
    
    return triangles
    



###############################################################################
# Read data:
#
#
datafile  = '/Users/clyne/Data/MPAS/MPAS_V4.0/x1.40962.output.2012-05-25_00.00.00.nc'
ds = xr.open_dataset(datafile, decode_times=False)




###############################################################################
# Plot variable on primary mesh:

projection = ccrs.PlateCarree(central_longitude=180.0)

fig, axs = plt.subplots(2,
                        1,
                        figsize=(7, 10),
                        subplot_kw={"projection": projection})
plt.tight_layout(pad=4, h_pad=-5)

var = ds.sst.isel(Time=0).values
xCell = rangeRestrict(np.rad2deg(ds.lonCell.values))
yCell = np.rad2deg(ds.latCell.values)
tris = ds.cellsOnVertex.values - 1

xCell, yCell, _ = projection.transform_points(ccrs.PlateCarree(), xCell, yCell).T
trisMask = makeBoundaryMask(xCell,tris,90.0)
triangles = Triangulation(xCell, yCell, triangles=tris, mask=~trisMask)

# Use global map and draw coastlines
axs[0].set_global()
axs[0].coastlines(linewidth=1.0, resolution="110m")
axs[0].set_aspect('equal')
axs[0].tripcolor(triangles,var,cmap='coolwarm' )
axs[0].set_title('triplot of MPAS primary mesh')

###############################################################################
# Plot variable on dual mesh:

var = ds.vorticity.isel(Time=0, nVertLevels=0).values
xVert = rangeRestrict(np.rad2deg(ds.lonVertex.values))
yVert = np.rad2deg(ds.latVertex.values)
verticesOnCell = ds.verticesOnCell.values - 1
nEdgesOnCell = ds.nEdgesOnCell.values
tris = triangulatePoly(verticesOnCell, nEdgesOnCell)

xVert, yVert, _ = projection.transform_points(ccrs.PlateCarree(), xVert, yVert).T
trisMask = makeBoundaryMask(xVert,tris,90.0)
triangles = Triangulation(xVert, yVert, triangles=tris, mask=~trisMask)

axs[1].set_global()
axs[1].coastlines(linewidth=1.0, resolution="110m")
axs[1].set_aspect('equal')
axs[1].tripcolor(triangles,var,cmap='coolwarm' )
axs[1].set_title('triplot of MPAS dual mesh')

plt.show()


