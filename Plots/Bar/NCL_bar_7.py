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


###############################################################################
# Create the plot data
x = [1, 2, 3, 4, 5, 6, 7, 8]
data = [154900, 56600, 40000, 30200, 29700, 24400, 21700, 13900]
labels = ['Lung', 'Colon/rectum', 'Breast', 'Prostate', 'Pancreas',  
          'Non-Hodgkin\'s Lymphoma', 'Leukemias', 'Ovary']

###############################################################################
# Create the custom colormap.
color_list = ['firebrick', 'red', 'orange', 'green', 'navy', 'blue', 'skyblue', 'slateblue']

###############################################################################
# Specify some plot settings.
plot_y_max = 180000
label_y_offset = 2000
label_rotation = 45
title = 'Estimated Cancer Deaths for 2002'
title_fontsize = 18

###############################################################################
# Create the first bar chart.
plt.bar(x, data, color=color_list)

for k, label in enumerate(labels):
    plt.text(x[k], data[k]+label_y_offset, label, rotation=label_rotation)

plt.ylim(top=plot_y_max)
plt.title(title, fontsize=title_fontsize)

# Suppress tick marks on the X axis.
plt.xticks([],[])
plt.show()

###############################################################################
# Create the second bar chart with a legend.

## NOTE: you may need to close the first figure window to see the second figure.
plt.figure(2)

bar_handle = plt.bar(x, data, color=color_list)
plt.legend(bar_handle, labels)
plt.ylabel("Number of Deaths")
plt.title(title, fontsize=title_fontsize)

# Suppress tick marks on the X axis.
plt.xticks([],[])
plt.show()
