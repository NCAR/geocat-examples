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
    """
    Utility function to create an array of coordinate tuples in GPS form (lon in degrees, lat in degrees)
    with the same dimensions as the pressure data, so each coordinate on the map can easily be mapped to
    the pressure data at that point.

    Args:

        None
            
    Returns: 
    
        coordarr (:class:`numpy.ndarray`):
            array of coordinate tuples in GPS form (lon in degrees, lat in degrees) 
            with the same dimensions as the pressure data.
            
    """
    coordarr = []
    for y in np.array(pressure.lat):
        temparr = []
        for x in np.array(pressure.lon):
            temparr.append((x, y))
        coordarr.append(temparr)
    return np.array(coordarr)

###############################################################################


def findCoordPressureData(coordarr, coord):
    """
    Utility function to find pressure at a coordinate in GPS form (lon in degrees, lat in degrees)

    Args:

        coordarr (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            with the same dimensions as the pressure data

        coord (:class:`tuple`):
            Ccoordinate tuple in GPS form (lon in degrees, lat in degrees)
            
    Returns: 
    
        pressure.data[x][y] (:class:`float`):
            Pressure value at the input coordinate
            
    """

    for x in range(len(coordarr)):
        for y in range(len(coordarr[x])):
            if coordarr[x][y][0] == coord[0] and coordarr[x][y][1] == coord[1]:
                return pressure.data[x][y]

###############################################################################


def getKClusters(arr):
    """
    Utility function to cluster coordinates using DBSCAN (Density-based spatial 
    clustering of applications with noise)

    Args:

        arr (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            where the pressure gradient equals 0
            
    Returns: 
    
        coordsAndLabels (:class:`dict`):
            Dictionary of cluster labels and coordinates in the form 
            {label (int): coordinates (list of tuples)}
            
    """

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

def findClusterExtrema(coordarr, coordsAndLabels, eType):
    """
    Utility function to find the minimums or maximums of each cluster of coordinates.

    Args:

        coordarr (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            with the same dimensions as the pressure data
            
        coordarr (:class:`dict`):
            Dictionary of cluster labels and coordinates in the form 
            {label (int): coordinates (list of tuples)}

        coordarr (:class:`str`): 'Min' or 'Max'
            'Min' argument will find Min of each cluster
            'Max' argument will find Max of each cluster
            
    
    Returns: 
    
        clusterExtremas (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees) 
            that specify either the Mins or Maxes of each labeled cluster
            
    """

    clusterExtremas = []

    for key in coordsAndLabels:

        pressures = []
        for coord in coordsAndLabels[key]:
            pressure = findCoordPressureData(coordarr, coord)
            pressures.append(pressure)

        if eType == 'Min':
            index = np.argmin(np.array(pressures))
        if eType == 'Max':
            index = np.argmax(np.array(pressures))

        clusterExtremas.append((coordsAndLabels[key][index][0], coordsAndLabels[key][index][1]))

    return clusterExtremas

###############################################################################


def findLocalMinima(minPressure=993):
    """
    Utility function to find local low pressure coordinates on a contour map

    Args:

        minPressure (:class:`int`):
            Pressure value that the local minimum pressures must be less than
            to quality as a low pressure location
    
    Returns: 
    
        clusterMins (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify low pressure areas
            
    """

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
    clusterMins = findClusterExtrema(coordarr, coordsAndLabels, eType='Min')

    return clusterMins

###############################################################################


def findLocalMaxima(maxPressure=1040):
    """
    Utility function to find local high pressure coordinates on a contour map

    Args:

        maxPressure (:class:`int`):
            Pressure value that the local maximum pressures must be greater than
            to quality as a high pressure location
    
    Returns: 
    
        clusterMaxs (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify high pressure areas
            
    """

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
    clusterMaxs = findClusterExtrema(coordarr, coordsAndLabels, eType='Max')

    return clusterMaxs


###############################################################################
# Helper function that will plot contour labels

def plotCLabels(contours, Clevels=[], lowClevels=[], highClevels=[]):
    """
    Utility function to plot contour labels

    Args:

        contours (:class:`cartopy.mpl.contour.GeoContourSet`):
            Contours that the labels will be plotted on

        Clevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with regular pressure values should be plotted

        highClevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with high pressure values should be plotted      

        lowClevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with low pressure values should be plotted       
    
    Returns: 
    
        None
            
    """
    print(contours)
    coordarr = makeCoordArr()

    if Clevels != []:
        geodeticClevels = GPStoGeodetic(Clevels)
        ax.clabel(contours, manual=geodeticClevels, inline=True, fontsize=14, colors='k', fmt="%.0f")

    if lowClevels != []:
        geodeticLowClevels = GPStoGeodetic(lowClevels)
        for x in range(len(geodeticLowClevels)):
            try:
                p = (int)(round(findCoordPressureData(coordarr, lowClevels[x])))
                plt.text(geodeticLowClevels[x][0], geodeticLowClevels[x][1], "L$_{" + str(p) + "}$", fontsize=22,
                         horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

    if highClevels != []:
        geodeticHighClevels = GPStoGeodetic(highClevels)
        for x in range(len(geodeticHighClevels)):
            try:
                p = (int)(round(findCoordPressureData(coordarr, highClevels[x])))
                plt.text(geodeticHighClevels[x][0], geodeticHighClevels[x][1], "H$_{" + str(p) + "}$", fontsize=22,
                horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

###############################################################################

def GPStoGeodetic(coords):
    """
    Utility function to transform GPS coordinates to geodetic coordinates

    Args:

        coords (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
    
    Returns:

        clevels (:class:`list`)
            List of coordinate tuples in geodetic form (geodetic longitude, geodetic latitude)

    """

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
