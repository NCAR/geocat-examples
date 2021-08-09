"""
NCL_box_2.py
============

This script illustrates the following concepts:
   - Drawing box plots
   - Manipulating boxplot visualizations
   - Manipulating plot axes

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/box_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/box_2_lg.png
"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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
# Helper function that will be released in GeoCAT-Viz. Delete this block after release.


def set_tick_direction_spine_visibility(ax,
                                        tick_direction='out',
                                        top_spine_visible=True,
                                        bottom_spine_visible=True,
                                        left_spine_visible=True,
                                        right_spine_visible=True):
    """Utility function to turn off axes spines and set tickmark orientations.

    Note: This function should be called after calling add_major_minor_ticks()

    Args:

        ax (:class:`matplotlib.axes._subplots.AxesSubplot` or :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`):
            Current axes to the current figure

        tick_direction (:class:`str`):
            Set 'in' to put ticks inside the axes,
            'out' to put ticks outside the axes,
            'inout' to put ticks both in and out of the axes.

        top_spine_visible (:class:`bool`):
            Set False to turn off top spine of the axes.

        bottom_spine_visible (:class:`bool`):
            Set False to turn off bottom spine of the axes.

        left_spine_visible (:class:`bool`):
            Set False to turn off left spine of the axes.

        right_spine_visible (:class:`bool`):
            Set False to turn off right spine.
    """
    ax.tick_params(direction=tick_direction, axis='both', which='both')
    ax.spines['top'].set_visible(top_spine_visible)
    ax.spines['bottom'].set_visible(bottom_spine_visible)
    ax.spines['left'].set_visible(left_spine_visible)
    ax.spines['right'].set_visible(right_spine_visible)

    if top_spine_visible and bottom_spine_visible:
        ax.xaxis.set_ticks_position('default')
    elif bottom_spine_visible and not top_spine_visible:
        ax.xaxis.set_ticks_position('bottom')
    elif top_spine_visible and not bottom_spine_visible:
        ax.xaxis.set_ticks_position('top')
    else:
        ax.xaxis.set_ticks_position('none')

    if left_spine_visible and right_spine_visible:
        ax.yaxis.set_ticks_position('default')
    elif not right_spine_visible and left_spine_visible:
        ax.yaxis.set_ticks_position('left')
    elif not left_spine_visible and right_spine_visible:
        ax.yaxis.set_ticks_position('right')
    else:
        ax.yaxis.set_ticks_position('none')


###############################################################################
# Helper function to set edge color of boxes


def setBoxColor(boxplot, colors):

    # Set edge color of the outside and median lines of the boxes
    for element in ['boxes', 'medians']:
        for box, color in zip(boxplot[element], colors):
            plt.setp(box, color=color)

    # Set the color of the whiskers and caps of the boxes
    for element in ['whiskers', 'caps']:
        for box, color in zip(
                zip(boxplot[element][::2], boxplot[element][1::2]), colors):
            plt.setp(box, color=color)


###############################################################################
# Plot:

# Create figure and axis
w = 0.1
fig, ax = plt.subplots(figsize=(6, 6))
boxplots = ax.boxplot(data,
                      labels=['Control', '-2Xna', '2Xna'],
                      widths=[w, w, w],
                      showfliers=False)

# Set whiskers style to dashed
plt.setp(boxplots['whiskers'], linestyle='--')

# Set boxplot edge colors
setBoxColor(boxplots, ['blue', 'red', '#66FF00'])

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax,
                                 ylim=(-6.0, 8.5),
                                 yticks=[-3.0, 0.0, 3.0, 6.0])

# Set y_axis format
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax,
                             y_minor_per_major=3,
                             x_minor_per_major=1,
                             labelsize=16)

# Use geocat.viz.util convenience function to set spines visibility
set_tick_direction_spine_visibility(ax,
                                    tick_direction='in',
                                    top_spine_visible=False,
                                    right_spine_visible=False)

# Use geocat.viz.util convenience function to add title to the plot axis.
gvutil.set_titles_and_labels(ax,
                             maintitle='Tailored Box Plot',
                             maintitlefontsize=22)

# Set padding between ticks and tick labels
ax.tick_params(pad=9)

# Display Plot
plt.tight_layout()
plt.show()
