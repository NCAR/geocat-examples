"""
NCL_sat_1.py
===============
This script illustrates the following concepts:
   - Creating an orthographic projection
   - Drawing line contours over a satellite map
   - Manually labeling contours
   - Transforming coordinates

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
"""

###############################################################################
# Import packages:
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from sklearn.cluster import KMeans, DBSCAN

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and
# load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"), decode_times=False)

# Get data from the 24th timestep
pressure = ds.slp[24, :, :]

# Translate short values to float values
pressure = pressure.astype('float64')

# Convert Pa to hPa data
pressure = pressure*0.01

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_pressure = gvutil.xr_add_cyclic_longitudes(pressure, "lon")

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
                plt.text(geodeticLowClevels[x][0], geodeticLowClevels[x][1], "L$_{" + str(p) + "}$", fontsize=16)
            except:
                continue

    if highClevels != []:
        geodeticHighClevels = transformCoords(lowClevels)
        for x in range(len(geodeticHighClevels)):
            try:
                p = (int)(round(findCoordPressureData(coordarr, highClevels[x][0], highClevels[x][1])))
                plt.text(geodeticHighClevels[x][0], geodeticHighClevels[x][1], "H$_{" + str(p) + "}$", fontsize=16)
            except:
                continue


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


def getKClusters(arr, numClusters):

    lonvals = [a_tuple[0] for a_tuple in arr]
    latvals = [a_tuple[1] for a_tuple in arr]

    '''
    ids = np.arange(1, len(latvals)+1)

    K_clusters = range(1, 10)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]

    firstCols = np.array(list(zip(ids, latvals, lonvals)))

    kmeans = KMeans(n_clusters=numClusters, init='k-means++')
    kmeans.fit(firstCols)
    labels = kmeans.predict(firstCols)
    '''

    db = DBSCAN(eps=5, min_samples=2) 
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

        tempmincoord = coordsAndLabels[key][0]
        tempminpressure = findCoordPressureData(coordarr,
                                                coordsAndLabels[key][0][0],
                                                coordsAndLabels[key][0][1])

        for coord in coordsAndLabels[key]:
            if findCoordPressureData(coordarr,
                                     coord[0],
                                     coord[1]) <= tempminpressure:

                tempmincoord = coord
                tempminpressure = findCoordPressureData(coordarr,
                                                        coord[0], coord[1])

        lonvalue = tempmincoord[0]
        latvalue = tempmincoord[1]

        clusterMins.append((lonvalue, latvalue))

    return clusterMins

###############################################################################
# Helper function that finds the local low pressure coordinates
# on a contour map.


def findLocalMinima(minPressure=980):

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

    coordsAndLabels = getKClusters(minimacoords, numClusters=8)
    clusterMins = findClusterMin(coordarr, coordsAndLabels)

    return clusterMins

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
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE, linewidth=.5)
ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')
ax.add_feature(cfeature.BORDERS, linewidth=.5)
ax.add_feature(cfeature.LAKES, facecolor='lightcyan',
               edgecolor='k', linewidth=.5)

# Make array of the contour levels that will be plotted
contours = np.arange(948, 1060, 4)
contours = np.append(contours, 975)
contours = np.sort(contours)

# Plot contour data
p = wrap_pressure.plot.contour(ax=ax,
                               transform=ccrs.PlateCarree(),
                               linewidths=0.5,
                               levels=contours,
                               cmap='black',
                               add_labels=False)

# regular pressure contour levels- These values were found by setting
# 'manual' argument in ax.clabel call to 'True' and then hovering mouse
# over desired location of countour label to find coordinate
# (which can be found in bottom left of figure window).
clevels = [(176.4, 34.63), (-150.46, 42.44), (-142.16, 28.5),
           (-134.12, 16.32), (-108.9, 17.08), (-98.17, 15.6),
           (-108.73, 42.19), (-111.25, 49.66), (-127.83, 41.93),
           (-92.49, 25.64), (-77.29, 29.08), (-77.04, 16.42),
           (-95.93, 57.59), (-156.05, 84.47), (-17.83, 82.52),
           (-76.3, 41.99), (-48.89, 41.45), (-33.43, 37.55),
           (-46.98, 17.17), (1.79, 63.67), (-58.78, 67.05),
           (-44.78, 53.68), (-69.69, 53.71), (-78.02, 52.22),
           (-16.91, 44.33), (-95.72, 35.17), (-102.69, 73.62)]

# low pressure contour levels- these will be plotted
# as a subscript to an 'L' symbol.
lowClevels = findLocalMinima()

# Plot Clabels
plotCLabels(p, Clevels=clevels, lowClevels=lowClevels)

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

# Make layout tight
plt.tight_layout()

plt.show()
