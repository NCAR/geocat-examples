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
data = np.random.lognormal(size=(40, 3), mean=1, sigma=.7)

for a in range(len(data)):
    data[a] = [x-4 for x in data[a]]

print(data)
fs = 10

###############################################################################
# Helper function to draw plots

def draw_plot(boxplot, number, edge_color):

    # Set edge color of boxes
    for element in ['boxes', 'medians']: #, 'whiskers', 'caps'
        plt.setp(boxplot[element][number], color=edge_color)

###############################################################################
# Plot:

fig, ax = plt.subplots(figsize=(6, 6))

boxplots = ax.boxplot(data, labels=['Control', '-2Xna', '2Xna'], showfliers=False) 

# Set whisker style to dashed
plt.setp(boxplots['whiskers'], linestyle='--')

draw_plot(boxplots, 0, 'blue')
draw_plot(boxplots, 1, 'red')
draw_plot(boxplots, 2, 'limegreen')

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax, ylim=(-6.0,9.0), yticks=[-3.0, 0.0, 3.0, 6.0])

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, y_minor_per_major=3, labelsize=14)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, maintitle='Box Plot with Polymarkers')

# Get rid of right and top values
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Add another axis 
ax2 = ax.inset_axes([0, 0, 1, 1])
ax2.patch.set_alpha(0.2)

ax2.set_xlim(0,6)
ax2.set_ylim(-6,9)

# Turn ticks in overlayed axis off
ax2.tick_params(top=False, bottom=False, left=False, right=False,
                labelleft=False, labelbottom=False)

# Get rid of right and top values
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

# Plot red x markers
ax2.scatter(1, 7.7, marker='x', color='red')
ax2.scatter(3, 2.5, marker='x', color='red')
ax2.scatter(5, 2, marker='x', color='red')

# Plot blue o markers
ax2.scatter(1, 2, marker='o', color='darkblue')
ax2.scatter(3, -0.5, marker='o', color='darkblue')
ax2.scatter(5, 1, marker='o', color='darkblue')


plt.show()