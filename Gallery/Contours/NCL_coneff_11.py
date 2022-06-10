"""
NCL_coneff_11.py
================
This script illustrates the following concepts:
   - Filling contours with multiple shaded patterns
   - Filling contours with stippling (solid dots)
   - Changing the size of the dot fill pattern in a contour plot
   - Overlaying a stipple pattern to show area of interest
   - Changing the density of contour shaded patterns

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/coneff_11.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/coneff_11_1_lg.png
                          https://www.ncl.ucar.edu/Applications/Images/coneff_11_2_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl

import geocat.datafiles as gdf
import geocat.viz as gv

###############################################################################
# Read in data

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/atmos.nc'), decode_times=False)

# Select meridional wind at lowest pressure level
v = ds.V.isel(time=0, lev=0)

###############################################################################
# Plot

# Generate figure (set its size (width, height) in inches)
plt.figure(figsize=(8, 10))
ax = plt.axes()

# Create a filled contour plot, using a NCL colormap
hatches = ['//////', '//////', '/////', '/////', None, '...', '..', '.', '.']
p = v.plot.contourf(ax=ax,
                    vmin=-45.0,
                    vmax=45,
                    levels=10,
                    add_colorbar=False,
                    hatches=hatches,
                    cmap='white')

# Choose colors for the hatches
colors = [
    'coral', 'palegreen', 'royalblue', 'lemonchiffon', 'white', 'fuchsia',
    'brown', 'cyan', 'mediumblue'
]
for i, collection in enumerate(p.collections):
    collection.set_edgecolor(colors[i % len(colors)])
    collection.set_linestyle('solid')
for collection in p.collections:
    collection.set_linewidth(0.)
    collection.set_linestyle('-')

# Plot the contour lines
c = v.plot.contour(ax=ax,
                   vmin=-45.0,
                   vmax=45,
                   levels=10,
                   colors='k',
                   linewidths=1,
                   add_colorbar=False)

# Add horizontal colorbar
cbar = plt.colorbar(p, orientation='horizontal', shrink=0.95, aspect=10)
cbar.ax.tick_params(labelsize=14)
cbar.set_ticks(np.arange(-35, 40, 10))
