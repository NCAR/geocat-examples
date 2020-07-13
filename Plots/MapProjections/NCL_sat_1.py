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

def findLocalExtrema(pressure, maxPressure=1040, minPressure=975, eType='Min'):
    """
    Utility function to find local low pressure coordinates on a contour map

    Args:

        pressure: (:class:`xarray.DataArray`):
            Xarray data array containing the lat and lon values

        maxPressure (:class:`int`):
            Pressure value that the local maximum pressures must be greater than
            to qualify as a high pressure location

        minPressure (:class:`int`):
            Pressure value that the local minimum pressures must be less than
            to qualify as a low pressure location

        eType (:class:`str`):
            'Min' or 'Max'
            Determines which extrema are being found- minimum or maximum,
            respectively
    
    Returns: 
    
        clusterMins (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees,
            lat in degrees)
            that specify low pressure areas
            
    """

    # Create a 2D array of all the coordinates with pressure data
    coordarr = []
    for y in np.array(pressure.lat):
        temparr = []
        for x in np.array(pressure.lon):
            temparr.append((x, y))
        coordarr.append(temparr)
    coordarr =  np.array(coordarr)

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

    extremacoords = []
    coordsinthearray = []

    # For every common zero in both gradient arrays
    for x in commonzeroes:

        try:
            xval = x[0]
            yval = x[1]

            if eType == 'Min':
                # If the gradient value is a "zero", and if the
                # pressure.data value is less than minPressure:
                if wrap_pressure.data[xval][yval] < minPressure:

                    coordonmap = coordarr[xval][yval]

                    coordsinthearray.append((xval, yval))

                    # Get coordinate from index in coordArr
                    xcoord = coordonmap[0]
                    ycoord = coordonmap[1]

                    extremacoords.append((xcoord, ycoord))

            if eType == 'Max':
                # If the gradient value is a "zero", and if the
                # pressure.data value is less than minPressure:
                if wrap_pressure.data[xval][yval] > maxPressure:

                    coordonmap = coordarr[xval][yval]

                    coordsinthearray.append((xval, yval))

                    # Get coordinate from index in coordArr
                    xcoord = coordonmap[0]
                    ycoord = coordonmap[1]

                    extremacoords.append((xcoord, ycoord))
        except:
            continue

    # coordsAndLabels = getKClusters(extremacoords)
    lonvals = [a_tuple[0] for a_tuple in extremacoords]
    latvals = [a_tuple[1] for a_tuple in extremacoords]
    
    db = DBSCAN(eps=10, min_samples=1) 
    new = db.fit(list(zip(lonvals, latvals)))
    labels = new.labels_
    
    # Create an dictionary of values with key being coordinate
    # and value being cluster label.
    coordsAndLabels = {}

    for x in range(len(extremacoords)):
        if labels[x] in coordsAndLabels:
            coordsAndLabels[labels[x]].append(extremacoords[x])
        else:
            coordsAndLabels[labels[x]] = [extremacoords[x]]

    clusterExtremas = []

    for key in coordsAndLabels:

        pressures = []
        for coord in coordsAndLabels[key]:

            for x in range(len(coordarr)):
                for y in range(len(coordarr[x])):
                    if coordarr[x][y][0] == coord[0] and coordarr[x][y][1] == coord[1]:
                        pval = pressure.data[x][y]

            pressures.append(pval)

        if eType == 'Min':
            index = np.argmin(np.array(pressures))
        if eType == 'Max':
            index = np.argmax(np.array(pressures))

        clusterExtremas.append((coordsAndLabels[key][index][0], coordsAndLabels[key][index][1]))

    return clusterExtremas

###############################################################################
# Helper function that will plot contour labels

def plotCLabels(pressure, contours, transform, Clevels=[], lowClevels=[], highClevels=[]):

    """
    Utility function to plot contour labels

    Args:

        pressure: (:class:`xarray.DataArray`):
            Xarray data array containing the lat and lon values

        contours (:class:`cartopy.mpl.contour.GeoContourSet`):
            Contours that the labels will be plotted on

        transform (:class:`cartopy._crs.Geodetic`):
            Projection that the input coordinates (in GPS form of lon, lat) should be transformed to

        Clevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with regular pressure values should be plotted  

        lowClevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with low pressure values should be plotted   

        highClevels (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with high pressure values should be plotted        
    
    Returns: 
    
        None
            
    """

    # Create coord arr to map to pressure values
    coordarr = []
    for y in np.array(pressure.lat):
        temparr = []
        for x in np.array(pressure.lon):
            temparr.append((x, y))
        coordarr.append(temparr)
    coordarr = np.array(coordarr)

    # Plot any regular contour levels
    if Clevels != []:
        clevelpoints = proj.transform_points(transform,
                                            np.array([x[0] for x in Clevels]),
                                            np.array([x[1] for x in Clevels]))
        transformedClevels = [(x[0], x[1]) for x in clevelpoints]
        ax.clabel(contours, manual=transformedClevels, inline=True, fontsize=14, colors='k', fmt="%.0f")

    # Plot any low contour levels
    if lowClevels != []:
        clevelpoints = proj.transform_points(transform,
                                            np.array([x[0] for x in lowClevels]),
                                            np.array([x[1] for x in lowClevels]))
        transformedLowClevels = [(x[0], x[1]) for x in clevelpoints]
        for x in range(len(transformedLowClevels)):
            try:
                # Find pressure data at that coordinate
                coord = lowClevels[x]
                for z in range(len(coordarr)):
                    for y in range(len(coordarr[z])):
                        if coordarr[z][y][0] == coord[0] and coordarr[z][y][1] == coord[1]:
                            p = int(round(pressure.data[z][y]))

                plt.text(transformedLowClevels[x][0], transformedLowClevels[x][1], "L$_{" + str(p) + "}$", fontsize=22,
                         horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

    # Plot any high contour levels
    if highClevels != []:
        clevelpoints = proj.transform_points(transform,
                                            np.array([x[0] for x in highClevels]),
                                            np.array([x[1] for x in highClevels]))
        transformedHighClevels = [(x[0], x[1]) for x in clevelpoints]
        for x in range(len(transformedHighClevels)):
            try:
                # Find pressure data at that coordinate
                coord = highClevels[x]
                for z in range(len(coordarr)):
                    for y in range(len(coordarr[z])):
                        if coordarr[z][y][0] == coord[0] and coordarr[z][y][1] == coord[1]:
                            p = int(round(pressure.data[z][y]))

                plt.text(transformedHighClevels[x][0], transformedHighClevels[x][1], "H$_{" + str(p) + "}$", fontsize=22,
                         horizontalalignment='center', verticalalignment='center', rotation=0)
            except:
                continue

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
lowClevels = findLocalExtrema(pressure, eType='Min')

# Plot Clabels
plotCLabels(pressure, p, ccrs.Geodetic(), Clevels=clevels, lowClevels=lowClevels)

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
