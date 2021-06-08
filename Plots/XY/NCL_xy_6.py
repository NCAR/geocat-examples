"""
NCL_xy_6.py
===========
This script illustrates the following concepts:
   - Changing the labels and tickmarks on the X axis in an XY plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_6.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/xy_6_lg.png
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

# Open a netCDF data file using xarray default engine and load data into xarray
ds = xr.open_dataset(gdf.get("netcdf_files/Jsst.nc"))

sst = ds.SST * 0.1
date = ds.date

# Dates in the file are represented by year and month (YYYYMM)
# representing them fractionally will make plotting the data easier
# This produces the same results as NCL's yyyymm_to_yyyyfrac() function
num_months = np.shape(date)[0]
date_frac = np.empty_like(date)
for n in np.arange(0, num_months, 1):
    yyyy = int(date[n] / 100)
    mon = (date[n] / 100 - yyyy) * 100
    date_frac[n] = yyyy + (mon - 1) / 12

###############################################################################
# Plot:

# Create a list of years
warm_yrs = [1951, 1953, 1957, 1963, 1965, 1969, 1972, 1976, 1982, 1987, 1991]

# Create a list of sst values corresponding to values in warm_yrs
y = []
for year in warm_yrs:
    index = int(np.where(np.round(date_frac, 3) == year)[0])
    y.append(sst[index])

# Create figure (setting figure size (width,height) in inches) and axes
plt.figure(figsize=(7, 6.5))
ax = plt.gca()

# Plot
plt.plot(warm_yrs, y)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=1,
                             y_minor_per_major=4,
                             labelsize=16)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, tick values, and tick labels
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(1951, 1991),
                                 ylim=(-1.5, 0.6),
                                 yticks=np.arange(-1.2, .6, .4),
                                 xticks=np.linspace(1951, 1991, 11),
                                 xticklabels=[
                                     '1951', '', '1957', '', '1965', '', '1972',
                                     '', '1982', '', '1991'
                                 ])

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax,
                             maintitle="Explicit axis labeling",
                             xlabel="",
                             ylabel="")

# Show the plot
plt.tight_layout()
plt.show()
