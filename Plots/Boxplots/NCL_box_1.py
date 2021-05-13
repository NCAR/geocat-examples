"""
NCL_box_1.py
===============

This script illustrates the following concepts:
   - Drawing box plots
   - Manipulating boxplot vizualizations
   - Manipulating plot axes

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/box_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/box_1_lg.png
"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import numpy as np
from geocat.viz import util as gvutil

###############################################################################
# Generate fake data:

seed = 200
np.random.seed(seed)

data = np.random.lognormal(size=(40, 3), mean=1, sigma=.7)
for a in range(len(data)):
    data[a] = [x - 4 for x in data[a]]

###############################################################################
# Plot:

# Create figure and axis
w = 0.25
fig, ax = plt.subplots(figsize=(6, 6))
boxplots = ax.boxplot(data,
                      labels=['Control', '-2Xna', '2Xna'],
                      widths=[w, w, w],
                      showfliers=False)

# Set whiskers style to dashed
plt.setp(boxplots['whiskers'], linestyle='--')

# Set median line to black
plt.setp(boxplots['medians'], color='black')

# Remove axis lines on top and right sides
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax,
                                 ylim=(-6.0, 9.0),
                                 yticks=[-3.0, 0.0, 3.0, 6.0])

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             y_minor_per_major=3,
                             x_minor_per_major=1,
                             labelsize=14)

# Use geocat.viz.util convenience function to add title to the plot axis.
gvutil.set_titles_and_labels(ax, maintitle='Default Box Plot')

# Make both major and minor ticks point inwards towards the plot
ax.tick_params(direction="in", which='both')

# Set ticks only at left and bottom sides of plot
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Display Plot
plt.show()
