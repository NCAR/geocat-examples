"""
NCL_sat_2.py
===============
This script illustrates the following concepts:
   - Unpacking 'short' data
   - Drawing filled contours over a satellite map
   - Explicitly setting contour fill colors
   - Finding local high pressure values

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_2_lg.png
"""

###############################################################################
# Import packages:
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as mticker

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and
# load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"), decode_times=False)

# Get data from the 21st timestep
pressure = ds.slp[21, :, :]

# Translate short values to float values
pressure = pressure.astype('float64')

# Convert Pa to hPa data
pressure = pressure*0.01

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_pressure = gvutil.xr_add_cyclic_longitudes(pressure, "lon")

###############################################################################
# Helper function that will return an array of (lon, lat) coord tuples
# with the same dimensions as the pressure data.


def makeCoordArr():

    coordarr = []
    for y in np.array(pressure.lat):
        temparr = []
        for x in np.array(pressure.lon):
            temparr.append((x, y))
        coordarr.append(temparr)
    return np.array(coordarr)

###############################################################################
# Helper function that will find the pressure at point (lon, lat).


def findCoordPressureData(coordarr, lon, lat):

    for x in range(len(coordarr)):
        for y in range(len(coordarr[x])):
            if coordarr[x][y][0] == lon and coordarr[x][y][1] == lat:
                return pressure.data[x][y]

###############################################################################
# Helper function that will cluster the array of coordinates
# into groups based on geographic location.
# Returns a dictionary of values in the form --> coordinate: cluster label.


def getKClusters(arr):

    lonvals = [a_tuple[0] for a_tuple in arr]
    latvals = [a_tuple[1] for a_tuple in arr]
    
    db = DBSCAN(eps=10, min_samples=1) 
    new = db.fit(list(zip(lonvals, latvals)))
    labels = new.labels_
    
    # Create an dictionary of values with key being coordinate
    # and value being cluster label.
    coordsAndLabels = {}

    for x in range(len(arr)):
        if labels[x] in coordsAndLabels:
            coordsAndLabels[labels[x]].append(arr[x])
        else:
            coordsAndLabels[labels[x]] = [arr[x]]

    return coordsAndLabels

###############################################################################
# Helper function that finds the minimum of each cluster of coordinates.


def findClusterMin(coordarr, coordsAndLabels):

    clusterMins = []

    for key in coordsAndLabels:

        minPressures = []
        for coord in coordsAndLabels[key]:
            minPressures.append(findCoordPressureData(coordarr,
                                                      coord[0],
                                                      coord[1]))


        minIndex = np.argmin(np.array(minPressures))
        tempmincoord = coordsAndLabels[key][minIndex]
        clusterMins.append((tempmincoord[0], tempmincoord[1]))

    return clusterMins

###############################################################################
# Helper function that finds the local low pressure coordinates
# on a contour map.


def findLocalMinima(minPressure=993):

    # Create a 2D array of all the coordinates with pressure data
    coordarr = makeCoordArr()

    # Set number that a derivative must be less than in order to
    # classify as a "zero"
    bound = 0.0

    # Get global gradient of contour data
    grad = np.gradient(wrap_pressure.data)

    # Gradient in the x direction
    arr1 = grad[0]

    # Gradient in the y direction
    arr2 = grad[1]

    # Get all array 1 indexes where gradient value is between -bound and +bound
    posfirstzeroes = np.argwhere(arr1 <= bound)
    negfirstzeroes = np.argwhere(-bound <= arr1)

    # Get all array 2 indexes where gradient value is between -bound and +bound
    possecondzeroes = np.argwhere(arr2 <= bound)
    negsecondzeroes = np.argwhere(-bound <= arr2)

    # Find zeroes of all four gradient arrays
    commonzeroes = []
    for x in possecondzeroes:
        if x in posfirstzeroes and x in negfirstzeroes and x in negsecondzeroes:
            commonzeroes.append(x)

    minimacoords = []
    coordsinthearray = []

    # For every common zero in both gradient arrays
    for x in commonzeroes:

        try:
            xval = x[0]
            yval = x[1]

            # If the gradient value is a "zero", and if the
            # pressure.data value is less than minPressure:
            if wrap_pressure.data[xval][yval] < minPressure:

                coordonmap = coordarr[xval][yval]

                coordsinthearray.append((xval, yval))

                # Get coordinate from index in coordArr
                xcoord = coordonmap[0]
                ycoord = coordonmap[1]

                minimacoords.append((xcoord, ycoord))
        except:
            continue

    coordsAndLabels = getKClusters(minimacoords)
    clusterMins = findClusterMin(coordarr, coordsAndLabels)

    return clusterMins

###############################################################################
# Helper function that finds the maximum of each cluster of coordinates.


def findClusterMax(coordarr, coordsAndLabels):

    clusterMaxs = []

    for key in coordsAndLabels:

        maxPressures = []
        for coord in coordsAndLabels[key]:
            maxPressures.append(findCoordPressureData(coordarr,
                                                      coord[0],
                                                      coord[1]))


        maxIndex = np.argmax(np.array(maxPressures))
        tempmaxcoord = coordsAndLabels[key][maxIndex]
        clusterMaxs.append((tempmaxcoord[0], tempmaxcoord[1]))

    return clusterMaxs

###############################################################################
# Helper function that finds the local high pressure coordinates
# on a contour map.


def findLocalMaxima(maxPressure=1040):

    # Create a 2D array of all the coordinates with pressure data
    coordarr = makeCoordArr()

    # Set number that a derivative must be less than in order to
    # classify as a "zero"
    bound = 0.0

    # Get global gradient of contour data
    grad = np.gradient(wrap_pressure.data)

    # Gradient in the x direction
    arr1 = grad[0]

    # Gradient in the y direction
    arr2 = grad[1]

    # Get all array 1 indexes where gradient value is between -bound and +bound
    posfirstzeroes = np.argwhere(arr1 <= bound)
    negfirstzeroes = np.argwhere(-bound <= arr1)

    # Get all array 2 indexes where gradient value is between -bound and +bound
    possecondzeroes = np.argwhere(arr2 <= bound)
    negsecondzeroes = np.argwhere(-bound <= arr2)

    # Find zeroes of all four gradient arrays
    commonzeroes = []
    for x in possecondzeroes:
        if x in posfirstzeroes and x in negfirstzeroes and x in negsecondzeroes:
            commonzeroes.append(x)

    maximacoords = []
    coordsinthearray = []

    # For every common zero in both gradient arrays
    for x in commonzeroes:

        try:
            xval = x[0]
            yval = x[1]

            # If the gradient value is a "zero", and if the
            # pressure.data value is greater than maxPressure:
            if wrap_pressure.data[xval][yval] >= maxPressure:

                coordonmap = coordarr[xval][yval]

                coordsinthearray.append((xval, yval))

                # Get coordinate from index in coordArr
                xcoord = coordonmap[0]
                ycoord = coordonmap[1]

                maximacoords.append((xcoord, ycoord))
        except:
            continue

    coordsAndLabels = getKClusters(maximacoords)
    clusterMaxs = findClusterMax(coordarr, coordsAndLabels)

    return clusterMaxs


###############################################################################
# Helper function that will plot contour labels

def plotCLabels(contours, Clevels=[], lowClevels=[], highClevels=[]):

    coordarr = makeCoordArr()

    if Clevels != []:
        geodeticClevels = transformCoords(Clevels)
        ax.clabel(contours, manual=geodeticClevels, inline=True, fontsize=14, colors='k', fmt="%.0f")

    if lowClevels != []:
        geodeticLowClevels = transformCoords(lowClevels)
        for x in range(len(geodeticLowClevels)):
            try:
                p = (int)(round(findCoordPressureData(coordarr, lowClevels[x][0], lowClevels[x][1])))
                plt.text(geodeticLowClevels[x][0], geodeticLowClevels[x][1], "L$_{" + str(p) + "}$", fontsize=22,
                         horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

    if highClevels != []:
        geodeticHighClevels = transformCoords(highClevels)
        for x in range(len(geodeticHighClevels)):
            try:
                p = (int)(round(findCoordPressureData(coordarr, highClevels[x][0], highClevels[x][1])))
                plt.text(geodeticHighClevels[x][0], geodeticHighClevels[x][1], "H$_{" + str(p) + "}$", fontsize=22,
                horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

###############################################################################
# Helper function that will transform lat/lon geographic coordinates 
# to geodetic coordinates

def transformCoords(coords):

    clevelpoints = proj.transform_points(ccrs.Geodetic(),
                                            np.array([x[0] for x in coords]),
                                            np.array([x[1] for x in coords]))
    clevels = [(x[0], x[1]) for x in clevelpoints]
    return clevels

###############################################################################
# Create plot

# Set figure size
fig = plt.figure(figsize=(8, 8))

# Set global axes with an orthographic projection
proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
ax = plt.axes(projection=proj)
ax.set_global()

# Add land, coastlines, and ocean features
ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=1)
ax.add_feature(cfeature.COASTLINE, linewidth=.3, zorder=2)
ax.add_feature(cfeature.OCEAN, facecolor='white')
ax.add_feature(cfeature.BORDERS, linewidth=.3)
ax.add_feature(cfeature.LAKES, facecolor='white',
               edgecolor='k', linewidth=.3)

# Create color map
colorvalues = [1020, 1036, 1500]
cmap = colors.ListedColormap(['None', 'lightgray', 'dimgrey'])
norm = colors.BoundaryNorm(colorvalues, 2)

# Plot contour data
p = wrap_pressure.plot.contourf(ax=ax,
                                zorder=2,
                                transform=ccrs.PlateCarree(),
                                levels=30,
                                cmap=cmap, norm=norm,
                                add_labels=False,
                                add_colorbar=False)

p = wrap_pressure.plot.contour(ax=ax,
                               transform=ccrs.PlateCarree(),
                               linewidths=0.3,
                               levels=30,
                               cmap='black',
                               add_labels=False)

# low pressure contour levels- these will be plotted
# as a subscript to an 'L' symbol.
lowClevels = findLocalMinima()
highClevels = findLocalMaxima()

# regular pressure contour levels- These values were found by setting
# 'manual' argument in ax.clabel call to 'True' and then hovering mouse
# over desired location of countour label to find coordinate
# (which can be found in bottom left of figure window).
clevels = [(-145.27, 50.9), (-125.89, 32.33), (-112.62, 19.89),
           (-139.31, 18.22), (-119.15, 51.02), (-85.22, 71.78),
           (-100.31, 18.73), (-97.75, 39.4), (-94.18, 51.19),
           (-81.94, 60.78), (-73.58, 47.14), (-99.6, 82.9), 
           (-55.75, 22.96), (-16.19, 46.72), (-137.39, 40.3),
           (-57.17, 49.07), (-62.17, 12.24), (-77.51, 32.42)]

# Label low, high, and regular contours
plotCLabels(p, Clevels=clevels, lowClevels=lowClevels, highClevels=highClevels)

# Use gvutil function to set title and subtitles
gvutil.set_titles_and_labels(ax,
                             maintitle=r"$\bf{SLP}$"+" "+r"$\bf{1963,}$"+" "+r"$\bf{January}$"+" "+r"$\bf{24th}$",
                             maintitlefontsize=20,
                             lefttitle="mean Daily Sea Level Pressure",
                             lefttitlefontsize=16,
                             righttitle="hPa",
                             righttitlefontsize=16)

# Set characteristics of text box
props = dict(facecolor='white', edgecolor='black', alpha=0.5)

# Place text box
ax.text(0.40, -0.1, 'CONTOUR FROM 948 TO 1064 BY 4',
        transform=ax.transAxes, fontsize=16, bbox=props)

# Add gridlines to axis
gl = ax.gridlines(color='gray', linestyle='--')
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 20))
gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 20))

# Make layout tight
plt.tight_layout()

plt.show()
