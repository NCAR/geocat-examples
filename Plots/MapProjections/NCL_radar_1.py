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
import matplotlib as mpl

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

##############################################################################
# Read in data:

ds = xr.open_dataset(gdf.get("netcdf_files/dz.nc"), decode_times=False)

# print(ds.DZ.data)
# print()
# print(ds.Azimuth.isel())
# print()
# print(ds.DZ.maxCells)

##############################################################################
# Convert data to radial form:

# Use a mesh grid
y = np.arange(0,240,0.25)
xx, yy = np.meshgrid(ds.Azimuth.data, y)


##############################################################################
# Plot:

fig = plt.figure(figsize=(10,8))

cmap = gvcmaps.gui_default

reflec = ds.DZ.plot.contourf(cmap=cmap, add_colorbar=False, vmin=-20, vmax=65, levels=np.arange(-20,70,5))


cbar = plt.colorbar(reflec, orientation="horizontal",
                    ticks=np.arange(-15, 65, 15))

plt.show()
