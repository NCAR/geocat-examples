"""
NCL_minmax_3.py
===============
This script illustrates the following concepts:
   - Calculating the local minima/maxima of your data
   - Adding text strings at local minima/maxima locations
   - Generating dummy data using "generate_2d_array"
   - Setting the background color for a text box
   - Turning on the perimeter of a text box

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/minmax_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/minmax_3_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from geocat.viz import util as gv
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Definition of generate_2d_array and helper functions adapted from
# https://github.com/NCAR/pyngl/blob/develop/src/ngl/__init__.py

#  Globals for random number generator for generate_2d_array
dfran_iseq = 0
dfran_rseq = [
    .749, .973, .666, .804, .081, .483, .919, .903, .951, .960, .039, .269,
    .270, .756, .222, .478, .621, .063, .550, .798, .027, .569, .149, .697,
    .451, .738, .508, .041, .266, .249, .019, .191, .266, .625, .492, .940,
    .508, .406, .972, .311, .757, .378, .299, .536, .619, .844, .342, .295,
    .447, .499, .688, .193, .225, .520, .954, .749, .997, .693, .217, .273,
    .961, .948, .902, .104, .495, .257, .524, .100, .492, .347, .981, .019,
    .225, .806, .678, .710, .235, .600, .994, .758, .682, .373, .009, .469,
    .203, .730, .588, .603, .213, .495, .884, .032, .185, .127, .010, .180,
    .689, .354, .372, .429
]


#  Random number generator for generate_2d_array.
def _dfran():
    global dfran_iseq
    global dfran_rseq
    dfran_iseq = dfran_iseq % 100
    r = dfran_rseq[dfran_iseq]
    dfran_iseq = dfran_iseq + 1
    return r


def generate_2d_array(dims, num_low, num_high, minv, maxv, seed=0):
    """Generates a "nice" 2D array of pseudo random data, especially for use in
    2D graphics.

    This function has the same effect as NCL generate_2d_array.

    Parameters
    ----------
    dims : tuple, list or array, int
        Dimensions of the two-dimensional array to be returned.
    num_low, num_high : int
        Integers representing the approximate minimum and maximum number of highs and lows
        that the output array will have. They must be in the range 1 to 25.
        If not, then they will be set to either 1 or 25.
    minv, maxv : float
        The exact minimum and maximum values that the output array will have.
    iseed : int, default to 0
        An optional argument specifying a seed for the random number generator.
        If iseed is outside the range 0 to 99, it will be set to 0.

    Returns
    -------
    out_array : numpy.ndarray
        A 2D array of pseudo random data.
    """

    # Globals for random numbers
    global dfran_iseq
    dfran_iseq = seed

    #  Dims are reversed in order to get the same results as the NCL function.
    nx = int(dims[1])
    ny = int(dims[0])
    # Column-major (Fortran-style) order in memory
    out_array = np.zeros([nx, ny], 'f')
    tmp_array = np.zeros([3, 25], 'f')
    fovm = 9. / float(nx)
    fovn = 9. / float(ny)
    # Make sure that num_low and num_high are between 1 to 25 inclusive
    nlow = max(1, min(25, num_low))
    nhgh = max(1, min(25, num_high))
    ncnt = nlow + nhgh

    # Fill up the temporary array
    for k in range(num_low):
        # lows at random locations.
        tmp_array[0, k] = 1. + (float(nx) - 1.) * _dfran()
        tmp_array[1, k] = 1. + (float(ny) - 1.) * _dfran()
        tmp_array[2, k] = -1.
    for k in range(num_low, num_low + num_high):
        # highs at random locations.
        tmp_array[0, k] = 1. + (float(nx) - 1.) * _dfran()
        tmp_array[1, k] = 1. + (float(ny) - 1.) * _dfran()
        tmp_array[2, k] = 1.

    # Initialize dmin and dmax to positive and negative infinity
    dmin = np.inf
    dmax = -np.inf
    # Initialize all values in out_array to average of minv and maxv
    midpt = 0.5 * (minv + maxv)
    out_array[:] = midpt

    # Populate out_array
    for j in range(ny):
        for i in range(nx):
            for k in range(ncnt):
                tempi = fovm * (float(i + 1) - tmp_array[0, k])
                tempj = fovn * (float(j + 1) - tmp_array[1, k])
                temp = -(np.square(tempi) + np.square(tempj))
                if (temp >= -20.):
                    out_array[i,j] = out_array[i,j] + \
                       0.5*(maxv - minv)*tmp_array[2,k]*np.exp(temp)
            dmin = min(dmin, out_array[i, j])
            dmax = max(dmax, out_array[i, j])

    out_array = (((out_array - dmin) / (dmax - dmin)) * (maxv - minv)) + minv
    out_array = np.transpose(out_array, [1, 0])

    del tmp_array

    return out_array


###############################################################################
# Helper function to add contour labels of local extrema with bounding boxes


def plotLabels(coord_locations, label):
    # Find contour value based on longitude and latitude coordinates
    for coord in coord_locations:
        # Note: second item of coord (lat) accesses the index for the row number,
        # and first item of coord (lon) access the index for the column number
        value = round(data.data[coord[1], coord[0]], 1)

        txt = ax.text(coord[0],
                      coord[1],
                      label + str(value),
                      fontsize=14,
                      horizontalalignment='center',
                      verticalalignment='center')
        txt.set_bbox(dict(facecolor='w', edgecolor='gray', pad=2))


###############################################################################
# Generate dummy data

nx = 100
ny = 100

data = generate_2d_array((nx, ny), 10, 10, -19., 16., 0)

# Convert data into type xarray.DataArray
data = xr.DataArray(data,
                    dims=["lat", "lon"],
                    coords=dict(lat=np.arange(nx), lon=np.arange(ny)))

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
plt.figure(figsize=(9.5, 8))

# Generate axes
ax = plt.axes()

# Set contour levels
levels = np.arange(-20, 18.5, 2.5)

# Plot data and create colorbar
cmap = gvcmaps.BlueYellowRed

# Plot filled contour and contour lines
contours = ax.contourf(data, cmap=cmap, levels=levels)
lines = ax.contour(contours, linewidths=0.5, linestyles='solid', colors='black')

# Find local min/max extrema with GeoCAT-Viz find_local_extrema
# Use below command instead after PR#46 in Viz is merged
# lmin = gv.find_local_extrema(data, eType='Low', highVal=12, lowVal=-10, eps=7)
lmin = gv.find_local_extrema(data, eType='Low', highVal=12, lowVal=-10)
lmax = gv.find_local_extrema(data, eType='High', highVal=12, lowVal=-10)

# Plot labels for local extrema
plotLabels(lmin, 'L')
plotLabels(lmax, 'H')

# Add colorbar
cbar = plt.colorbar(contours,
                    ax=ax,
                    orientation='vertical',
                    shrink=0.96,
                    pad=0.06,
                    extendrect=True,
                    extendfrac='auto',
                    aspect=15,
                    drawedges=True,
                    ticks=levels[1:-1:])  # set colorbar levels

# Set every other tick labels to be integers
ticklabs = cbar.ax.get_yticklabels()
[
    ticklabs[i].set_text(ticklabs[i].get_text()[:-2])
    for i in range(1, len(ticklabs), 2)
]

# Center align colorbar tick labels
cbar.ax.set_yticklabels(ticklabs, ha='center')
cbar.ax.yaxis.set_tick_params(pad=26, length=0, labelsize=16)

# Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
gv.set_axes_limits_and_ticks(ax,
                             xlim=(0, 99),
                             ylim=(0, 99),
                             xticks=np.arange(0, 100, 20),
                             yticks=np.arange(0, 100, 20))

# Use geocat.viz.util convenience function to add minor and major tick lines
gv.add_major_minor_ticks(ax,
                         x_minor_per_major=4,
                         y_minor_per_major=4,
                         labelsize=16)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gv.set_titles_and_labels(ax,
                         maintitle='Adding your own minima/maxima text strings',
                         maintitlefontsize=24)

# Set different tick font sizes and padding for X and Y axis
ax.tick_params(axis='both', pad=10)

# Set axes to be square
ax.set_aspect(aspect='equal')

# Show plot
plt.tight_layout()
plt.show()
