"""
NCL_resampling_1.py
===================

Contributed by:
   - Brian Medeiros (@brianpm)

Originally published:
   - https://github.com/brianpm/hacknostics/blob/master/Notebooks/bootstrapping_like_ncl.ipynb

This script illustrates the following concepts:
   -

See following URLs to see the reproduced NCL plots & script:
    - Original NCL script: https://ncl.ucar.edu/Applications/Scripts/resampling_1.ncl
    - Original NCL plots: http://ncl.ucar.edu/Applications/Images/resampling_1_1_lg.png, http://ncl.ucar.edu/Applications/Images/resampling_1_2_lg.png, and http://ncl.ucar.edu/Applications/Images/resampling_1_3_lg.png

"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import numpy as np

#%%
# These distributions of sampling indices illustrate properties of resampling with replacement from a uniform
# distribution using generate_sample_indices. Clearly, a reasonably large N is needed to 'reasonably' sample all
# combinations.
#
# NCL's `resampling_1.ncl` example is slightly confusing, at least partly because NCL has some idiosyncratic defaults.
#
# The NS array is not just the sample size, but it is also being used to specify the interval from which integers are
# being drawn. I think this is to be thought of as like drawing indices from a sample with NS entries. This can be a
# little confusing because in the loop, NCL is generating arrays of indices of size NS drawn from the range [0,NS].
#
# The NCL function generate_sample_indices uses random_uniform. In our implementation, we will use the modern Numpy
# infrastructure that uses integers to generate integer random numbers from a discrete uniform distribution. Another
# advantage her is that the Generator also has a choice method allowing us to replicate NCL's functionality with no
# effort.
#
# The NCL example produces 3 plots that are just realizations of the same process. While I guess that shows that you
# don't get the same answer every time, I don't think it is necessary. Our example will make one instance of the
# 8-panel plot.


def generate_sample_indices(N, method=True, rng=None, minval=None, maxval=None):
    """Return an array of length N of integer indices derived by sampling with
    or without replacement.

       [0,N) or [minval, maxval].

    N : number of indices to return
    method : determine whether to sample with replacement (True) or not (False).
    rng : random number generator
        If rng is provided, use the `choice` method on that random number generator.
        If rng is None, use Numpy's `defaut_rng` to instantiate a fresh random number generator.

    minval and maxval : used to specify the range of values (i.e. indices) to use.
        This is useful when the sample size is different from the total data size,
        for example, if you want to select 250 values from an array that is 10_000_000 elements.

    Example Application:
        If want to sample a distribution with sequences of a given length,
        specify maxval = len(data) - len(sequence)
    """

    if rng is None:
        rng = np.random.default_rng()  # Numpy's default Generator
    if minval is not None:
        mn = minval
    else:
        mn = 0
    if maxval is not None:
        mx = maxval
    else:
        mx = N
    if (minval is not None) or (maxval is not None):
        arr = np.arange(mn, mx)
    else:
        arr = N
    return rng.choice(arr, size=N, replace=method)


# Original NCL Code is often provided in comments.
# Some lines are directly modified to python syntax, but often it is written in more idiomatic python.
#
# ;***********************************************************
# ; resampling_1.ncl
# ;
# ; Concepts illustrated:
# ;   - Generating random number seeds based on a 'clock'
# ;   - Generate 'resampling with replacement' indices
# ;     Use: generate_sample_indices( N, 1 )
# ;   - Use histogram to display distribution
# ;   - create a panel plot
# ;***********************************************************
# ;--- Specify sample sizes
# ;***********************************************************

NS = np.array([25, 100, 500, 1000, 5000, 10000, 100000, 1000000])

#   NP    = len(NS)                              # NCL --> not needed in Python version
#   plot  = new (NP, "graphic", "No_FillValue")  #

# *********************************************************** --- Generate and use random number seeds for
# initialization *********************************************************** NCL defaults to fixed seeds for its
# random number generator, but that is not the case for Numpy, so re-seeding is not strictly necessary. Numpy has
# fairly advanced random number generation features (https://numpy.org/doc/stable/reference/random/index.html).

# NCL:
#  rand1 = toint(systemfunc(" date +%s")) # --> NCL uses the system's date command

# Python:
# Method 1 (subprocess to use OS date just like NCL)
# import subprocess
# cmd = subprocess.run(['date', '+%s'], capture_output=True)
# rand1 = int(cmd.stdout)
# If you don't want to use the OS (directly) to get the date, you could use Python:
# Method 2 (datetime):
from datetime import datetime

curr_time = datetime.now()
rand1 = int(curr_time.strftime('%s'))
# Note: Method 1 and Method 2 produce the same result.

rand2 = int((54321 * rand1) % 2147483398)
#   NCL : random_setallseed(rand1, rand2)  # the ncl RNG uses two integers for seeding
# Python/Numpy:
# We can use a sequence (of any length) to seed.
# If no seed is given, "fresh, unpredictable entropy will be pulled from the OS" <-- Means we didn't need to worry about trying to make up a new seed.
rng = np.random.default_rng(seed=[rand1,
                                  rand2])  # rng = random number generator

# NCL Code from example
# ***********************************************************
# --- Plot a histogram of index distributions for each sample size
#
# ***********************************************************
#  wks  = gsn_open_wks ("png","resampling")  ; send graphics to PNG file
#  gsn_define_colormap(wks,"default")  ; 30 distinct colors
#  resh           = True
#  resh@gsnDraw   = False
#  resh@gsnFrame  = False
#  resh@tmXBLabelStride = 1
#  resh@tiMainOffsetYF  = -0.020       ; move tiMain down into plot
# ;resh@gsnHistogramBinWidth = ?? ; for 'tuning' ... if desired
# ***********************************************************
# --- Loop
# ***********************************************************
#   do plotnum=0,2
#     do np=0,NP-1
#        iw := generate_sample_indices( NS(np), 1 )
#        iw@long_name = "N="+NS(np)
#        printMinMax(iw, 0)
#        resh@tiMainString = iw@long_name
#        delete(iw@long_name)  ; do not want on plot
#        if (np.eq.0 .or. np.eq.4) then      ; reduce clutter
#            resh@tiYAxisString = "Frequency"
#        else
#          resh@tiYAxisString = " "         ; No title on Y axis.
#        end if
#        plot(np) = gsn_histogram(wks, iw  ,resh)
#     end do
#   resP                        = True
#   resP@gsnMaximize            = True
#   resP@gsnPanelMainString     = "Distribution: Uniform Random Indices w/ Replacement"
#   resP@gsnPanelLeft           = 0.01  ; make room on left and right side of paneled
#   resP@gsnPanelRight          = 0.99  ; plots for text and tickmarks
#   gsn_panel(wks,plot,(/2,4/),resP)
#   end do

# Python using Numpy and Matplotlib
fig, ax = plt.subplots(figsize=(12, 6),
                       ncols=4,
                       nrows=2,
                       sharey=False,
                       constrained_layout=True)
aa = ax.ravel()  # makes a view of ax that can be indexed with one number.
iw = dict(
)  # hold the results all together // This is optional, but could be useful if there are more steps than
# just making the histogram.
histograms = dict()
h_edges = dict()
for i, ns in enumerate(NS):
    print(f"i = {i}, ns = {ns}")
    iw[ns] = generate_sample_indices(ns, method=True, rng=rng)
    histograms[ns], h_edges[ns] = np.histogram(
        iw[ns])  # keep histogram counts and bin edges.
    aa[i].bar(h_edges[ns][0:-1] + np.diff(h_edges[ns]),
              histograms[ns],
              width=0.8 * np.diff(h_edges[ns])[1])
    aa[i].set_title(f"N = {ns}")

plt.setp(ax[:, 0], ylabel="FREQUENCY")  # put labels on left side axes.
plt.show()
