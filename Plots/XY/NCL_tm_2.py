"""
NCL_tm_2.py
===============
Tickmark and Axis Manipulation example

This Python script reproduces the NCL plot script found here: https://www.ncl.ucar.edu/Applications/Scripts/tm_2.ncl
"""


###############################################################################
# Import the necessary python libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

###############################################################################
# Define a function for creating an array of random values.


def random_floats(low, high, size):
    values = [np.random.uniform(low, high) for _ in range(size)]
    return values


###############################################################################
# Create the plot data.
# Note that range() top value is not included in the returned array of values.

x_data = np.arange(1950, 2006)
y_data = np.random.uniform(-4, 4, 56)

# Print out a formatted message; note the starting 'f' for the string.
print(f"There are { len(x_data) } values in x_data, and { len(y_data) } values in y_data.")


###############################################################################
# Make a subplot with major ticks that are multiples of 5.
# Label major ticks with '%d' formatting but don't label minor ticks.

# Figure size is (width, height) inches.
plt.figure(1, figsize=(8, 6))

# Create a subplot grid with two rows and one column (stacked subplots), and
# set the current plot context to the top subplot.
ax1 = plt.subplot(2, 1, 1)

# Format the tick labels.
# For the minor ticks, use no labels; defaults to NullFormatter.
ax1.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Set the major tick spacing.
major_tick_spacing = 5
ax1.xaxis.set_major_locator(MultipleLocator(major_tick_spacing))
spacingString = f'Tick Spacing = {major_tick_spacing}'

# Draw ticks on all sides of the plot.
plt.tick_params(which='both', top=True, right=True)

# Increase the length of the tick marks.
plt.tick_params(which='major', length=10.0)
plt.tick_params(which='minor', length=5.0)

# Set the minor tick spacing for X and Y axes.
ax1.xaxis.set_minor_locator(MultipleLocator(1.25))
ax1.yaxis.set_minor_locator(MultipleLocator(0.5))

# Add a descriptive string to the top left corner of the plot.
ax1.text(0.01, 1.1, spacingString, transform=ax1.transAxes, fontWeight='bold')

# Plot the line and set the X axis limits.
plt.plot(x_data, y_data, color='black', linewidth=0.5)
plt.xlim((1949, 2006))

###############################################################################
# Make a subplot with major ticks that are set to explicit values and minor ticks that
# are multiples of 1.

# Set the current plot context to the bottom subplot.
ax2 = plt.subplot(2, 1, 2)

# Set the tick locations on the X axis.
xtick_locations = [1950, 1960, 1970, 1980, 1990, 2000, 2005]
plt.xticks(xtick_locations, fontSize=12)

# Format the tick labels.
# For the minor ticks, use no labels; defaults to NullFormatter.
ax2.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Draw ticks on all sides of the plot.
plt.tick_params(which='both', top=True, right=True)

# Increase the length of the tick marks.
plt.tick_params(which='major', length=10.0)
plt.tick_params(which='minor', length=5.0)

# Set the minor tick spacing for X and Y axes.
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.yaxis.set_minor_locator(MultipleLocator(0.5))

# Add a descriptive string to the top left corner of the plot.
ax2.text(0.01, 1.1, "Ticks Set Explicitly", transform=ax2.transAxes, fontWeight='bold')

# Plot the line and set the X axis limits.
plt.plot(x_data, y_data, color='black', linewidth=0.5)
plt.xlim((1949, 2006))

# Create more space between subplots
plt.subplots_adjust(hspace=0.4)

# Draw the entire plot on the screen.
plt.show()
