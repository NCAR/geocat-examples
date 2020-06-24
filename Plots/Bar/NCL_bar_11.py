"""
NCL_bar_11.py
===============
This script illustrates the following concepts:
   - Drawing filled bars using solid colors
   - Changing the aspect ratio of a bar plot
   - Setting the minimum/maximum value of the X and Y axis in a bar plot
   - Overlaying XY plots on each other
   - Paneling bar plots  
   - Drawing a custom labelbar

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_11.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/bar_11_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np

from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil


###############################################################################
# Generate dummy data:
num_months = 12
bars_per_panel = 4
panels = 4
data = np.random.uniform(0.1, 1.15, (panels, bars_per_panel, num_months))

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
          'Nov', 'Dec']
###############################################################################
# Plot:
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
x = np.arange(len(months)) # where to draw x ticks
width = 0.2 # width of each bar within the groups

# Use geocat.viz.util convenience function to set axes parameters
gvutil.set_axes_limits_and_ticks(axs[0][0], ylim=(0.4, 1.2),
                                 xticks=x,
                                 yticks=np.arange(0.4, 1.4, 0.2),
                                 xticklabels=months)
# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(axs[0][0], x_minor_per_major=1,
                             y_minor_per_major=4, labelsize=9)
# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(axs[0][0], ylabel='(\u00B0C)', labelfontsize=12)

# Add data to first subplot
axs[0][0].bar(x-width*3/2, data[0][0][:], width, edgecolor='black',
              linewidth=0.25, color='red', label='first')
axs[0][0].bar(x-width/2, data[0][1][:], width, edgecolor='black',
              linewidth=0.25, color='lightsteelblue', label='second')
axs[0][0].bar(x+width/2, data[0][2][:], width, edgecolor='black',
              linewidth=0.25, color='blue', label='third')
axs[0][0].bar(x+width*3/2, data[0][3][:], width, edgecolor='black',
              linewidth=0.25, color='lime', label='fourth')

# Add legend with `figlegend()` to position it relative to figure instead of subplots
handles, labels = axs[0][0].get_legend_handles_labels()
fig.legend(handles, labels, ncol=4, loc='lower center', fontsize=14, columnspacing=5, frameon=False)

plt.show()