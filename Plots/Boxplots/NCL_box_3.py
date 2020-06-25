"""
NCL_box_3.py
===============

This script illustrates the following concepts:
   - Drawing box plots
   - Adding markers to a box plot
   - Setting the color of individual boxes in a box plot
   - Setting the width of individual boxes in a box plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/box_3.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/box_3_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import matplotlib.pyplot as plt

from geocat.viz import util as gvutil

###############################################################################
# Generate fake data

np.random.seed(200)
data = np.random.lognormal(size=(40, 3), mean=0, sigma=1)
fs = 10

###############################################################################
# Plot:

fig, ax = plt.subplots(figsize=(6, 6))

flierprops = dict(marker='o', markerfacecolor='darkblue', markersize=10,
                  linestyle='none', markeredgecolor='r')

ax.boxplot(data, labels=['Control', '-2Xna', '2Xna'], meanprops=flierprops, meanline=False, showmeans=True)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax, ylim=(-6.0,9.0), yticks=[-3.0, 0.0, 3.0, 6.0])

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=5, labelsize=14)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, maintitle='Box Plot with Polymarkers')

plt.show()