"""
NCL_bar_7.py
===============
Concepts illustrated:
  - Drawing filled bars
  - Filling the bars in a bar plot with different colors
  - Setting the minimum/maximum value of the Y axis in a bar plot
  - Adding text to a plot
  - Rotating text 45 degrees
  - Drawing a custom legend

This Python script reproduces the NCL plot script found here:  https://www.ncl.ucar.edu/Applications/Scripts/bar_7.ncl
"""

###############################################################################
# Import the necessary python libraries
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import warnings
warnings.filterwarnings("ignore")


###############################################################################
# Create the plot data
x = [1, 2, 3, 4, 5, 6, 7, 8]
data = [154900, 56600, 40000, 30200, 29700, 24400, 21700, 13900]
labels = ['Lung', 'Colon/rectum', 'Breast', 'Prostate', 'Pancreas',  
          'Non-Hodgkin\'s Lymphoma', 'Leukemias', 'Ovary']

###############################################################################
# Create the custom color list.
color_list = ['firebrick', 'red', 'orange', 'green', 'navy', 'blue', 'skyblue', 'slateblue']

###############################################################################
# Specify some plot settings.

# Title settings
title = 'Estimated Cancer Deaths for 2002'
title_fontsize = 16

# Axis Settings
plot_y_max = 180_000

# Tick Settings
major_tick_spacing = 30_000
minor_tick_spacing = 10_000
tick_label_fontsize = 12
tick_length_multiplier = 2

# Label Settings
label_rotation = 45
label_y_offset = 2000

###############################################################################
# Create the first bar chart.

# Figure size is (width, height) inches.
plt.figure(1, figsize=(6, 5))

plt.bar(x, data, color=color_list, edgecolor='black')
plt.title(title, fontsize=title_fontsize)

# Add a rotated label to each bar.
for k, label in enumerate(labels):
    plt.text(x[k], data[k]+label_y_offset, label, rotation=label_rotation)


# Draw ticks on three sides of the plot.  Suppress tick labels on the bottom.
plt.tick_params(which='both', top=True, right=True, left=True, bottom=False, labelsize=tick_label_fontsize)
plt.xticks([], [])

# Set the tick spacing and limits for the Y axis.
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(major_tick_spacing))
ax.yaxis.set_minor_locator(MultipleLocator(minor_tick_spacing))

# Increase the tick mark lengths by some factor.
y_major_tick_length = plt.rcParams["ytick.major.size"]
y_minor_tick_length = plt.rcParams["ytick.minor.size"]
plt.tick_params(which='major', length=y_major_tick_length * tick_length_multiplier)
plt.tick_params(which='minor', length=y_minor_tick_length * tick_length_multiplier)

# Set the limits for the Y axis.
plt.ylim(top=plot_y_max)

# Draw plot on the screen.
plt.show()


###############################################################################
# Create the second bar chart with a legend.


## NOTE: you may need to close the first figure window to see the second figure.
# Figure size is (width, height) inches.
plt.figure(2, figsize=(6, 5))

bar_handle = plt.bar(x, data, color=color_list, edgecolor='black')
plt.ylabel("Number of Deaths", fontsize=16)
plt.title(title, fontsize=title_fontsize)

# Reverse the legend ordering to match NCL.
bars_reversed = bar_handle[::-1]
labels_reversed = labels[::-1]

# Add the legend.
plt.legend(bars_reversed, labels_reversed)

# Draw ticks on three sides of the plot.  Suppress tick labels on the bottom.
plt.tick_params(which='both', top=True, right=True, left=True, bottom=False, labelsize=tick_label_fontsize)
plt.xticks([], [])

# Set the tick spacing and limits for the Y axis.
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(major_tick_spacing))
ax.yaxis.set_minor_locator(MultipleLocator(minor_tick_spacing))

# Increase the tick mark lengths by some factor.
y_major_tick_length = plt.rcParams["ytick.major.size"]
y_minor_tick_length = plt.rcParams["ytick.minor.size"]
plt.tick_params(which='major', length=y_major_tick_length * tick_length_multiplier)
plt.tick_params(which='minor', length=y_minor_tick_length * tick_length_multiplier)

# Set the limits for the Y axis.
plt.ylim(top=plot_y_max)

# Move the figure left border, so Y Label appears without manually adjusting the viewport.
plt.subplots_adjust(left=0.2)

# Draw plot on the screen.
plt.show()
