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


NS = np.array([25, 100, 500, 1000, 5000, 10000, 100000, 1000000])

# If you don't want to use the OS (directly) to get the date, you could use Python:
# Method 2 (datetime):
from datetime import datetime

curr_time = datetime.now()
rand1 = int(curr_time.strftime('%s'))
# Note: Method 1 and Method 2 produce the same result.

rand2 = int((54321 * rand1) % 2147483398)

# We can use a sequence (of any length) to seed.
# If no seed is given, "fresh, unpredictable entropy will be pulled from the OS" <-- Means we didn't need to worry about trying to make up a new seed.
rng = np.random.default_rng(seed=[rand1,
                                  rand2])  # rng = random number generator

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
