"""
NCL_bar_1.py
===============
This script illustrates the following concepts:
   - Drawing bars instead of curves in an XY plot
   - Changing the aspect ratio of a bar plot
   - Drawing bars up or down based on a Y reference value

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/bar_1_1_lg.png, https://www.ncl.ucar.edu/Applications/Images/bar_1_2_lg.png
                         and https://www.ncl.ucar.edu/Applications/Images/bar_1_3_lg.png
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

# Open a netCDF data file using xarray default engine and load the data
ds = xr.open_dataset(gdf.get("netcdf_files/soi.nc"))
date = ds.date
dsoik = ds.DSOI_KET
dsoid = ds.DSOI_DEC

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
# Plot

# Generate figure (set its size (width, height) in inches) and axes
fig = plt.figure(constrained_layout=True, figsize=(7, 7))
axes = fig.subplots(nrows=3)

# Set baseline as the minimum excluding the invalid values in the array
baseline = np.nanmin(dsoik[::8])

# Create barplot
axes[0].bar(date_frac[::8],
            dsoik[::8] - baseline,
            align='center',
            edgecolor='black',
            color='white',
            width=8 / 12,
            linewidth=.5,
            bottom=-1.75)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axes[0],
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(axes[0],
                                 yticks=np.arange(-2.0, 2.0, 0.5),
                                 xlim=(date_frac[40], date_frac[-16]),
                                 xticks=np.linspace(1900, 1980, 5))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(axes[0], maintitle="Bar plot")

# Create barplot
axes[1].bar(
    date_frac[::8],
    dsoik[::8],
    color='none',
)

# Create barplot
axes[2].bar(date_frac[::8],
            dsoik[::8],
            align='edge',
            edgecolor='black',
            color='white',
            width=8 / 12,
            linewidth=.5)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axes[2],
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=12)

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(axes[2],
                                 yticks=np.arange(-2.0, 2.0, 0.5),
                                 xlim=(date_frac[40], date_frac[-16]),
                                 xticks=np.linspace(1900, 1980, 5))

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(axes[2],
                             maintitle="Bar plot with a reference line")

# Show the plot
plt.show()
