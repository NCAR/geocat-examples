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
from sklearn.cluster import DBSCAN
import warnings

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
# Define a helper function to find local extrema

def findLocalExtrema(da, highVal=0, lowVal=1000, eType='Low'):
    """
    Utility function to find local low/high field variable coordinates on a contour map. To classify as a local high, the data
    point must be greater than highVal, and to classify as a local low, the data point must be less than lowVal.

    Args:
        da: (:class:`xarray.DataArray`):
            Xarray data array containing the lat, lon, and field variable (ex. pressure) data values
        highVal (:class:`int`):
            Data value that the local high must be greater than to qualify as a "local high" location.
            Default highVal is 0.
        lowVal (:class:`int`):
            Data value that the local low must be less than to qualify as a "local low" location.
            Default lowVal is 1000.
        eType (:class:`str`):
            'Low' or 'High'
            Determines which extrema are being found- minimum or maximum, respectively.
            Default eType is 'Low'.
    Returns:
        clusterExtremas (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify local low/high locations
    """

    # Create a 2D array of coordinates in the same shape as the field variable data
    # so each coordinate is easily mappable to a data value
    # ex:
    # (1, 1), (2, 1), (3, 1)
    # (1, 2)................
    # (1, 3)................
    lons, lats = np.meshgrid(np.array(da.lon), np.array(da.lat))
    coordarr = np.dstack((lons, lats))

    # Find all zeroes that also qualify as low or high values
    extremacoords = []

    if eType == 'Low':
        coordlist = np.argwhere(da.data < lowVal)
        extremacoords = [tuple(coordarr[x[0]][x[1]]) for x in coordlist]
    if eType == 'High':
        coordlist = np.argwhere(da.data < lowVal)
        extremacoords = [tuple(coordarr[x[0]][x[1]]) for x in coordlist]

    if extremacoords == []:
        if eType == 'Low':
            warnings.warn('No local extrema with data value less than given lowVal')
            return []
        if eType == 'High':
            warnings.warn('No local extrema with data value greater than given highVal')
            return []

    # Clean up noisy data to find actual extrema

    # Use Density-based spatial clustering of applications with noise
    # to cluster and label coordinates
    db = DBSCAN(eps=10, min_samples=1)
    new = db.fit(extremacoords)
    labels = new.labels_

    # Create an dictionary of values with key being coordinate
    # and value being cluster label.
    coordsAndLabels = {label: [] for label in labels}
    for label, coord in zip(labels, extremacoords):
        coordsAndLabels[label].append(coord)

    # Initialize array of coordinates to be returned
    clusterExtremas = []

    # Iterate through the coordinates in each cluster
    for key in coordsAndLabels:

        # Create array to hold all the field variable values for that cluster
        datavals = []
        for coord in coordsAndLabels[key]:

            # Find pressure data at that coordinate
            cond = np.logical_and(coordarr[:, :, 0] == coord[0], coordarr[:, :, 1] == coord[1])
            x, y = np.where(cond)
            datavals.append(da.data[x[0]][y[0]])

        # Find the index of the smallest/greatest field variable value of each cluster
        if eType == 'Low':
            index = np.argmin(np.array(datavals))
        if eType == 'High':
            index = np.argmax(np.array(datavals))

        # Append the coordinate corresponding to that index to the array to be returned
        clusterExtremas.append((coordsAndLabels[key][index][0], coordsAndLabels[key][index][1]))

    return clusterExtremas

###############################################################################
# Define a helper function that will plot contour labels

def plotCLabels(da, contours, transform, ax, proj, clabel_locations=[], fontsize=12, whitebbox=False, horizontal=False):

    """
    Utility function to plot contour labels by passing in a coordinate to the clabel function.
    This allows the user to specify the exact locations of the labels, rather than having matplotlib
    plot them automatically.

    Args:
        da: (:class:`xarray.DataArray`):
            Xarray data array containing the lat, lon, and field variable data values.
        contours (:class:`cartopy.mpl.contour.GeoContourSet`):
            Contour set that is being labeled.
        transform (:class:`cartopy._crs`):
            Instance of CRS that represents the source coordinate system of coordinates.
            (ex. ccrs.Geodetic()).
        ax (:class:`matplotlib.pyplot.axis`):
            Axis containing the contour set.
        proj (:class:`cartopy.crs`):
            Projection 'ax' is defined by.
            This is the instaance of CRS that the coordinates will be transformed to.
        clabel_locations (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contours with regular field variable values should be plotted.
        fontsize (:class:`int`):
            Font size of contour labels.
        whitebbox (:class:`bool`):
            Setting this to "True" will cause all labels to be plotted with white backgrounds
        horizontal (:class:`bool`):
            Setting this to "True" will cause the contour labels to be horizontal.
    Returns:
        cLabels (:class:`list`):
            List of text instances of all contour labels
    """

    # Initialize empty array that will be filled with contour label text objects and returned
    cLabels = []

    # Plot any regular contour levels
    if clabel_locations != []:
        clevelpoints = proj.transform_points(transform,
                                             np.array([x[0] for x in clabel_locations]),
                                             np.array([x[1] for x in clabel_locations]))
        transformed_locations = [(x[0], x[1]) for x in clevelpoints]
        ax.clabel(contours, manual=transformed_locations, inline=True, fontsize=fontsize, colors='k', fmt="%.0f")
        [cLabels.append(txt) for txt in contours.labelTexts]

        if horizontal is True:
            [txt.set_rotation('horizontal') for txt in contours.labelTexts]

    if whitebbox is True:
        [txt.set_bbox(dict(facecolor='w', edgecolor='none', pad=2)) for txt in cLabels]

    return cLabels

###############################################################################
# Define a helper function that will plot contour labels

def plotELabels(da, contours, transform, ax, proj, clabel_locations=[], eType='Low', fontsize=22, horizontal=True, whitebbox=False):

    """
    Utility function to plot contour labels. High/Low contour labels will be plotted using text boxes for more accurate label values
    and placement.

    Args:
        da: (:class:`xarray.DataArray`):
            Xarray data array containing the lat, lon, and field variable data values.
        contours (:class:`cartopy.mpl.contour.GeoContourSet`):
            Contour set that is being labeled.
        transform (:class:`cartopy._crs`):
            Instance of CRS that represents the source coordinate system of coordinates.
            (ex. ccrs.Geodetic()).
        ax (:class:`matplotlib.pyplot.axis`):
            Axis containing the contour set.
        proj (:class:`cartopy.crs`):
            Projection 'ax' is defined by.
            This is the instaance of CRS that the coordinates will be transformed to.
        clabel_locations (:class:`list`):
            List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
            that specify where the contour labels should be plotted.
        type (:class:`list`):
            'high' or 'low'
            High contour labels will be plotted with an H
            Low contour labels will be plotted with an L
        fontsize (:class:`int`):
            Font size of regular contour labels.
        horizontal (:class:`bool`):
            Setting this to "True" will cause the contour labels to be horizontal.
        whitebbox (:class:`bool`):
            Setting this to "True" will cause all labels to be plotted with white backgrounds
    Returns:
        extremaLabels (:class:`list`):
            List of text instances of all contour labels
    """

    # Create array of coordinates in the same shape as field variable data
    # so each coordinate can be easily mapped to its data value.
    # ex:
    # (1, 1), (2, 1), (3, 1)
    # (1, 2)................
    # (1, 3)................
    lons, lats = np.meshgrid(np.array(da.lon), np.array(da.lat))
    coordarr = np.dstack((lons, lats))

    # Initialize empty array that will be filled with contour label text objects and returned
    extremaLabels = []

    # Plot any low contour levels
    clabel_points = proj.transform_points(transform,
                                          np.array([x[0] for x in clabel_locations]),
                                          np.array([x[1] for x in clabel_locations]))
    transformed_locations = [(x[0], x[1]) for x in clabel_points]

    for x in range(len(transformed_locations)):

        try:
            # Find field variable data at that coordinate
            coord = clabel_locations[x]
            cond = np.logical_and(coordarr[:, :, 0] == coord[0], coordarr[:, :, 1] == coord[1])
            z, y = np.where(cond)
            p = int(round(da.data[z[0]][y[0]]))

            if eType == 'High':
                lab = plt.text(transformed_locations[x][0], transformed_locations[x][1], "H$_{" + str(p) + "}$", fontsize=fontsize,
                               horizontalalignment='center', verticalalignment='center')
            elif eType == 'Low':
                lab = plt.text(transformed_locations[x][0], transformed_locations[x][1], "L$_{" + str(p) + "}$", fontsize=fontsize,
                               horizontalalignment='center', verticalalignment='center')

            if horizontal is True:
                lab.set_rotation('horizontal')

            extremaLabels.append(lab)

        except:
            continue

    if whitebbox is True:
        [txt.set_bbox(dict(facecolor='w', edgecolor='none', pad=2)) for txt in extremaLabels]

    return extremaLabels


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
contours = np.arange(948, 1072, 4)

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
regularCLabels = [(176.4, 34.63), (-150.46, 42.44), (-142.16, 28.5),
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
lowCLabels = findLocalExtrema(pressure, eType='Low', highVal=1040, lowVal=975)

# Plot Clabels
plotCLabels(pressure, p, ccrs.Geodetic(), ax, proj, clabel_locations=regularCLabels)
plotELabels(pressure, p, ccrs.Geodetic(), ax, proj, clabel_locations=lowCLabels, eType='Low')

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
