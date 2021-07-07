"""
NCL_corel_1.py
==============
This script illustrates the following concepts:
   - Calculating a cross correlation
   - Generating an equally-spaced span of integers

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/corel_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/corel_1_lg.png
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

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
                     decode_times=False)

#extract time series from 3d data
ts = ds.TS
ts1 = ts[:, 45, 64]
ts2 = ts[:, 23, 117]

# Set lag
maxlag = 25

# Calculate cross correlations
ccr = np.correlate(ts1, ts2, mode='ful')
x = np.arange(0, maxlag, 1)

###############################################################################
# LeadLag function from https://www.researchgate.net/publication/255696651_PythonNCL_free_alternatives_for_Earth_Scientists


def LeadLagCorr(A, B, nlags=25):
    coefs = np.empty(nlags + 1)
    cpt = 0
    for p in range(-nlags // 2, nlags // 2, 1):
        if p < 0:
            Aint = A[:p]
            Bint = B[-p:]
        elif p == 0:
            Aint = A
            Bint = B
        else:
            Aint = A[p:]
            Bint = B[:-p]

        n = len(Aint)
        sA = np.std(Aint)
        sB = np.std(Bint)
        mA = np.mean(Aint)
        mB = np.mean(Bint)

        r = np.sum((Aint - mA) * (Bint - mB)) / ((n - 1) * sA * sB)
        coefs[cpt] = r

        cpt = cpt + 1

    return coefs


###############################################################################
# Plot:

# Create figure (setting figure size (width,height) in inches) and axes
plt.figure(figsize=(7, 6.5))
ax = plt.axes()

ccr = LeadLagCorr(ts1, ts2)

ax.plot(ccr, color='black', linewidth=0.5)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             x_minor_per_major=4,
                             y_minor_per_major=5,
                             labelsize=16)

# Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
# Set axes limits, tick values, and tick labels to show latitude & longitude (i.e. North (N) - South (S))
# gvutil.set_axes_limits_and_ticks(
#     ax,
#     xlim=(0, 24),
#     ylim=(-1.2, 1.2),
#     xticks=x[::4])

# Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
gvutil.set_titles_and_labels(ax,
                             maintitle="37.7N 180E vs 23.72S 149W",
                             xlabel="LAG")

# Set major and minor tick directions inward
ax.tick_params(which='both', direction='in')

# Show plot
plt.tight_layout()
plt.show()
