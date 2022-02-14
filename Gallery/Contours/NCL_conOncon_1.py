"""
NCL_conOncon_1.py
=================
This script illustrates the following concepts:
   - Drawing pressure/height contours on top of another set of contours
   - Drawing negative contour lines as dashed lines
   - Drawing the zero contour line thicker
   - Changing the color of a contour line
   - Overlaying dashed contours on solid line contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/conOncon_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/conOncon_1_lg.png
"""

################################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/mxclim.nc"))
# Extract variables
U = ds.U[0, :, :]
V = ds.V[0, :, :]

################################################################################
# Plot:

# Generate figure (set its size (width, height) in inches) and axes
plt.figure(figsize=(12, 12))
ax = plt.gca()

# Set y-axis to have log-scale
plt.yscale('log')

# Contour-plot U-data
p = U.plot.contour(ax=ax, levels=16, colors='red', extend='neither')
ax.clabel(p, fmt='%d', inline=1, fontsize=14)

# Contour-plot V-data
p = V.plot.contour(ax=ax, levels=16, colors='blue', extend='neither')
ax.clabel(p, fmt='%d', inline=1, fontsize=14)

# Use geocat.viz.util convenience function to set axes tick values
# Set y-lim inorder for y-axis to have descending values
gvutil.set_axes_limits_and_ticks(ax,
                                 xticks=np.linspace(-60, 60, 5),
                                 xticklabels=['60S', '30S', '0', '30N', '60N'],
                                 ylim=ax.get_ylim()[::-1],
                                 yticks=U["lev"])

# Change formatter or else we tick values formatted in exponential form
ax.yaxis.set_major_formatter(ScalarFormatter())

# Tweak label sizes, etc.
ax.yaxis.label.set_size(20)
ax.tick_params('both', length=20, width=2, which='major', labelsize=18)
ax.minorticks_off()

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax,
                             maintitle="Ensemble Average 1987-89",
                             maintitlefontsize=20,
                             lefttitle=U.long_name,
                             lefttitlefontsize=18,
                             righttitle=U.units,
                             righttitlefontsize=18,
                             xlabel="")

# Create second y-axis to show geo-potential height.
# Currently we're using bogus values for height, cause we haven't figured out how to make this work.
axRHS = ax.twinx()
dummy = 10
mn, mx = ax.get_ylim()
axRHS.set_ylim(mn * dummy, mx * dummy)
axRHS.set_ylim(axRHS.get_ylim()[::-1])
axRHS.set_ylabel('Height (km)')
axRHS.yaxis.label.set_size(20)
axRHS.tick_params('both', length=20, width=2, which='major', labelsize=18)

# Show the plot
plt.tight_layout()
plt.show()
