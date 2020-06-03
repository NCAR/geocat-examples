"""
NCL_xy_5.py
===============
This script illustrates the following concepts:
   - Adding a separate curve to an XY plot using gsn_polyline
   - Drawing a Y reference line in an XY plot
   - Filling the areas of an XY curve above and below a reference line
   - Changing the width and height of a plot
   - Creating a new date array to use in a plot
   - Using named colors to indicate a fill color
   - Changing the title on the Y axis
   - Creating a main title
   - Changing the size/shape of an XY plot using viewport resources
   - Setting the mininum/maximum value of the Y axis in an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_5_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/soi.nc"))
dsoik = ds.DSOI_KET
dsoid = ds.DSOI_DEC
date = ds.date

# Creating a new date array for x axis labels
datedim = np.shape(date)[0]
new_date = np.empty_like(date)

for n in np.arange(0, datedim, 1):
    yyyy = date[n]/100
    mon = date[n]-yyyy*100
    new_date[n] = yyyy + (mon-1)/12

print(new_date)
###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(8, 4))
ax = plt.gca()

# Plot data
ax.fill_between(dsoik.time, dsoik, where=dsoik>0, color='red')
ax.fill_between(dsoik.time, dsoik, where=dsoik<0, color='blue')
dsoid.plot(ax=ax, color='black')

# Plot reference line
plt.plot([0, datedim], [0, 0], color='grey')

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=4, 
                             labelsize=14)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(ax, ylim=(-3, 3), 
                                     yticks=np.linspace(-3, 3, 7),
                                     yticklabels=np.linspace(-3, 3, 7),
                                     xlim=(0, datedim),
                                     xticks=np.arange(0, datedim, 12*20),
                                     xticklabels=np.arange(1880, 1995, 20))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle="Darwin Southern Oscillation Index", xlabel='', ylabel='')

plt.show()

