"""
NCL_vector_5.py
===============
 A vector pressure/height plot

This script illustrates the following concepts:
   - Drawing pressure/height vectors over filled contours
   - Interpolate to user specified pressure levels
   - Drawing curly vectors
   - Thinning vectors using a minimum distance resource
   - Using the geocat-comp method `interp_hybrid_to_pressure <https://geocat-comp.readthedocs.io/en/latest/user_api/generated/geocat.comp.interp_hybrid_to_pressure.html#geocat.comp.interp_hybrid_to_pressure>`_

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/vector_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/vector_5_lg.png
"""

###############################################################################
# Import packages:

import xarray as xr
from matplotlib import pyplot as plt
import numpy as np

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil
from geocat.comp import interp_hybrid_to_pressure

###############################################################################
# Read in data:
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)

# Define an array of surface pressures
pnew = np.arange(200, 901, 50)

# Read in variables
P0mb = 1000.
hyam = ds.hyam  # get a coefficiants
hybm = ds.hybm  # get b coefficiants
PS = ds.PS  # get pressure

# Read in variables from data interpolated to pressure levels
# interp_hybrid_to_pressure is the Python version of vinth2p in NCL script
T = interp_hybrid_to_pressure(data=ds.T,
                              ps=PS,
                              hyam=hyam,
                              hybm=hybm,
                              p0=P0mb,
                              new_levels=pnew,
                              method='log')
W = interp_hybrid_to_pressure(data=ds.OMEGA,
                              ps=PS,
                              hyam=hyam,
                              hybm=hybm,
                              p0=P0mb,
                              new_levels=pnew,
                              method='log')
V = interp_hybrid_to_pressure(data=ds.V,
                              ps=PS,
                              hyam=hyam,
                              hybm=hybm,
                              p0=P0mb,
                              new_levels=pnew,
                              method='log')

# Extract data
t = T.isel(time=0).sel(lon=170, method="nearest")
w = W.isel(time=0).sel(lon=170, method="nearest")
v = V.isel(time=0).sel(lon=170, method="nearest")

wscaler = np.mean(W)
vscaler = np.mean(V)
scale = abs(vscaler / wscaler)

wscale = w * scale

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 10))

# Generate axes using Cartopy and draw coastlines
ax = plt.axes()

# Specify which contours should be drawn
levels = np.linspace(200, 300, 11)

# # Plot contour lines
t.plot.contour(ax=ax,
               levels=levels,
               colors='black',
               linewidths=0.5,
               linestyles='solid',
               add_labels=False)

# # Plot filled contours
colors = t.plot.contourf(ax=ax,
                         levels=levels,
                         cmap='magma',
                         add_labels=False,
                         add_colorbar=False)

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, labelsize=16)

# Use geocat.viz.util convenience function to set axes tick values
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(-90, 90),
                                 ylim=(900, 200),
                                 xticks=np.arange(-60, 61, 30),
                                 yticks=np.array(
                                     [200, 250, 300, 400, 500, 700, 850]),
                                 xticklabels=['60S', '30S', '0', '30N', '60N'])

# Turn off minor ticks on Y axis
ax.tick_params(axis='y', which='minor', left=False)

# Draw vector plot
# (there is no matplotlib equivalent to "CurlyVector" yet)
Q = plt.quiver(t['plev'],
               t['lat'],
               v.data,
               wscale.data,
               color='black',
               zorder=1,
               pivot="middle",
               width=0.001)

# # Draw legend for vector plot
# ax.add_patch(
#     plt.Rectangle((150, -140),
#                   30,
#                   30,
#                   facecolor='white',
#                   edgecolor='black',
#                   clip_on=False))
