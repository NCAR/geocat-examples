"""
NCL_bar_5.py
===========
This script illustrates the following concepts:
    - Drawing multiple sets of filled bar charts up or down based on Y reference values
    - Drawing bar charts
    - Changing the labels and tickmarks in a bar plot
    - Adding labels to the right Y axis

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_5.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/bar_5_lg.png
"""

###############################################################################
# Import packages

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data
ds = xr.open_dataset(gdf.get("netcdf_files/Jsst.nc"))
sst = ds.SST
date = ds.date

#scale the sst variable to range from around -1 to 1
sst = sst * .1

# Dates in the file are represented by year and month (YYYYMM)
# representing them fractionally will make plotting the data easier
# This produces the same results as NCL's yyyymm_to_yyyyfrac() function
num_months = np.shape(date)[0]
date_frac = np.empty_like(date)
for n in np.arange(0, num_months, 1):
    yyyy = int(date[n] / 100)
    mon = (date[n] / 100 - yyyy) * 100
    date_frac[n] = yyyy + (mon - 1) / 12

###############################################################################
# Plot:

# Create two lists of values: one for years represented and another for Y values
# in inches of the bottom left corner of year graph
warm = [1951, 1953, 1957, 1963, 1965, 1969, 1972, 1976, 1982, 1987, 1991]
heights_list = [
    0.52, 0.764, 1.0, 1.25, 1.5135, 1.721, 2.0, 2.215, 2.5345, 2.72, 2.98
]


# A helper function to create a figure with multiple axes, each of which will have a different bar graph
def create_figure(width, num_subplots, heights_list):
    # Create global variables for the figures and an empty dictionary to store the axes
    global fig, ax0, ax_dict
    ax_dict = {}

    # Create figure and default axis which will be visible
    fig = plt.figure(figsize=(width + 2, (num_subplots / 4) + 2))
    ax0 = fig.add_axes([0.5, 0.5, width, num_subplots / 4])

    # Loop through heights in heights_list and create a different axis in ax_dict
    # for each one
    i = 1
    for height in heights_list:
        ax_dict["ax" + str(i)] = fig.add_axes(
            [0.355, height, width + .295, 0.25 * .75])
        i = i + 1


# A helper function to create a bar chart for each axis
def bar_plot(ax_name, year):
    # Find year limits of each bar chart
    year_start = year - 1
    year_end = year + 3

    # Find the indices for each of the year limits
    year_istart = int(np.where(np.round(date_frac, 3) == year_start)[0])
    year_iend = int(np.where(np.round(date_frac, 3) == year_end)[0])

    # Create each bar chart where it is red if it is above 0 and blue if below
    ax_dict[ax_name].bar(date_frac[year_istart:year_iend],
                         sst[year_istart:year_iend],
                         align='edge',
                         edgecolor='black',
                         color=[
                             'red' if (value > 0) else 'blue'
                             for value in sst[year_istart:year_iend]
                         ],
                         width=.08,
                         linewidth=2)
    # Turn off axis so it is not visible
    ax_dict[ax_name].axis("off")


# A helper function to make the left y axis labels
def left_tick_labels(num_plots):
    tick_list = []
    i = 0
    tick_list.append("")
    while i < num_plots:
        tick_list.append("-1.0")
        tick_list.append("0.0")
        tick_list.append("1.0")
        tick_list.append("")
        i = i + 1
    tick_list.append("")
    return tick_list


# A helper function to make the right y axis labels
def right_tick_labels(year_list):
    tick_list = []
    tick_list.append("")
    for year in year_list:
        tick_list.append("")
        tick_list.append(year)
        tick_list.append("")
        tick_list.append("")
    tick_list.append("")
    return tick_list


# Create axes and bar charts by looping through axes dictionary and warm years
create_figure(3, 11, heights_list)
for ax, year in zip(ax_dict, warm):
    bar_plot(ax, year)

# Create right y axis by cloning the left side
axRHS = ax0.twinx()

# Make a variable for the degree symbol
degree = u"\u00b0"

# Use geocat.viz.util convenience function to add titles to the center and right of the plot axis
gvutil.set_titles_and_labels(ax0,
                             maintitle="Monthly SST Anomalies for Nino-3",
                             maintitlefontsize=50,
                             righttitle=("(" + degree + "C)"),
                             righttitlefontsize=39)
# Add center title
ax0.text(0.38, 1.05, 'Warm Events', fontsize=38, transform=ax0.transAxes)

# Use geocat.viz.util convenience function to add major tick lines
gvutil.add_major_minor_ticks(ax0, x_minor_per_major=1, y_minor_per_major=1)

# Create the lists for the left and right axes
left_y_ticks = left_tick_labels(11)
right_y_ticks = right_tick_labels(11, warm)

# Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(
    ax0,
    xlim=(-3, 3),
    xticks=np.linspace(-3, 3, 7),
    xticklabels=["Jan₋₁", "Jul₋₁", "Jan₀", "Jan₀", "Jan₊₁", "Jul₊₁", "Jan₊₂"],
    yticks=np.linspace(0, 46, 46),
    yticklabels=left_y_ticks)
gvutil.set_axes_limits_and_ticks(axRHS,
                                 yticks=np.linspace(0, 46, 46),
                                 yticklabels=right_y_ticks)

# Set tick parameters for all axes
ax0.tick_params(axis="x", size=28, labelsize=30)
ax0.tick_params(axis="y", size=14, labelsize=20)
axRHS.tick_params(axis="y", size=14, labelsize=20)

# Show plot
plt.show()

###############################################################################
# Although the code above does recreate the NCL plot, it is tedious to replicate
# it in Python. A different process to use is subplots, which, in the
# specific example below, each have their own axes. This not only makes the graph
# easier to read, but is much simpler to recreate. The subplot method is shown
# below.

###############################################################################
# Plot utilizing the subplot method:

# Create the figure with figure size (height, width) in inches
fig2, ax2 = plt.subplots(11, 1, figsize=(12, 24))

# Loop through all of the years and plot them as a bar chart
i = 0
for year in warm:
    # Find year limits of each bar chart
    year_start = year - 1
    year_end = year + 3

    # Find the indicies for each of the year limits
    year_istart = int(np.where(np.round(date_frac, 3) == year_start)[0])
    year_iend = int(np.where(np.round(date_frac, 3) == year_end)[0])

    # Create each bar chart where it is red if it is above 0 and blue if below
    ax2[i].bar(date_frac[year_istart:year_iend],
               sst[year_istart:year_iend],
               align='edge',
               edgecolor='black',
               color=[
                   'red' if (value > 0) else 'blue'
                   for value in sst[year_istart:year_iend]
               ],
               width=.08,
               linewidth=1)

    # Set ticks and limits for axes using convenience function
    gvutil.set_axes_limits_and_ticks(ax2[i],
                                     xlim=((year_start), year_end),
                                     xticks=np.linspace(year_start, year_end,
                                                        5),
                                     ylim=(-3, 3.5),
                                     yticks=np.linspace(-2, 2, 3))

    # Use geocat.viz.util convenience function to add major tick lines
    gvutil.add_major_minor_ticks(ax2[i],
                                 x_minor_per_major=4,
                                 y_minor_per_major=2)

    # Create right hand side axis, add the year as a title to the axis, and remove labels
    ax2RHS = ax2[i].twinx()
    ax2RHS.set_ylabel(str(year), size=14, fontweight='bold')
    ax2RHS.set_yticklabels([])
    i = i + 1

# Adjust the white space between each subplot
plt.subplots_adjust(hspace=.4)

# Make a variable for the degree symbol
degree = u"\u00b0"

# Add title to entire figure
fig2.suptitle("Monthly SST Anomalies for Nino-3",
              horizontalalignment='center',
              y=0.93,
              fontsize=26,
              fontweight='bold')

# Add subtitles
fig2.text(0.42, .9, 'Warm Events', fontsize=24)
fig2.text(0.12, .9, "(" + degree + "C)", fontsize=24)

plt.show()
