"""
NCL_radar_1.py
===============
This script illustrates the following concepts:
   - Calculating deviation from zonal mean
   - Drawing zonal average plots
   - Moving the contour informational label into the plot
   - Changing the background color of the contour line labels
   - Spanning part of a color map for contour fill
   - Making the colorbar be vertical
   - Paneling four subplots in a two by two grid using `gridspec`
   - Changing the aspect ratio of a subplot
   - Drawing color-filled contours over a cylindrical equidistant map
   - Using a blue-white-red color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/radar_1.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/radar_1_1_lg.png
                          https://www.ncl.ucar.edu/Applications/Images/radar_1_2_lg.png
"""

##############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

##############################################################################
# Read in data:

ds = xr.open_dataset(gdf.get("netcdf_files/dz.nc"), decode_times=False)

##############################################################################
# Convert data to radial form:

# Designate center of radial data
xcenter = 0.0
ycenter = 0.0

# construct radial array from netcdf metadata
km_between_cells = 0.25
radius = ds.DZ.data.shape[1] * km_between_cells
r = np.arange(0, radius, 0.25)

values = ds.DZ.data

# Make angles monotonic
theta = ds.Azimuth.data
theta[0:63] = theta[0:63] - 360

radius_matrix, theta_matrix = np.meshgrid(r, theta)
X = radius_matrix * np.cos(theta_matrix)
Y = radius_matrix * np.sin(theta_matrix)


##############################################################################
# Plot:

fig, ax = plt.subplots(figsize=(8, 10))

cmap = gvcmaps.gui_default

p = plt.scatter(X, Y, c=values, cmap=cmap, marker=',', s=1)

cbar = plt.colorbar(p,
                    orientation="horizontal",
                    ticks=np.arange(-15, 65, 15))


# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, labelsize=12)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax,
                             lefttitle=ds.DZ.long_name,
                             lefttitlefontsize=16,
                             righttitle=ds.DZ.units,
                             righttitlefontsize=16,
                             xlabel="",
                             ylabel="")

plt.show()
