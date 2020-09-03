"""
NCL_panel_10.py
===============
This script illustrates the following concepts:
   - Drawing Hovmueller plots
   - Attaching plots along the Y axis
   - Using a blue-white-red color map
   - Drawing zonal average plots
   - Paneling attached plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_10.ncl and https://www.ncl.ucar.edu/Applications/Scripts/panel_attach_10.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_10_lg.png and https://www.ncl.ucar.edu/Applications/Images/panel_attach_10_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine
# and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/chi200_ud_smooth.nc'))

lon = ds.lon
times = ds.time
scale = 1000000
chi = ds.CHI
chi = chi / scale

###############################################################################
# Creat Single Plot:
fig, (ax1, ax2) = plt.subplots(nrows=1,
                               ncols=2,
                               sharey=True,
                               figsize=(12, 9),
                               gridspec_kw=dict(wspace=0,
                                                width_ratios=[0.75, 0.25],
                                                left=0.15,
                                                right=0.85,
                                                top=0.85,
                                                bottom=0.15))
# Create inset axes for color bar
cax1 = inset_axes(ax1,
                  width='100%',
                  height='7%',
                  loc='lower left',
                  bbox_to_anchor=(0, -0.15, 1, 1),
                  bbox_transform=ax1.transAxes,
                  borderpad=0)

# Draw contour lines
ax1.contour(lon,
            times,
            chi,
            levels=np.arange(-12, 13, 2),
            colors='black',
            linestyles='solid',
            linewidths=.5)

# Draw filled contours
cf = ax1.contourf(lon,
                  times,
                  chi,
                  levels=np.arange(-12, 13, 2),
                  cmap=gvcmaps.BlWhRe)

# Draw colorbar with larger tick labels
cbar = plt.colorbar(cf, cax=cax1, orientation='horizontal', ticks=np.arange(-10, 11, 2))
cbar.ax.tick_params(labelsize=12)

# Use geocat.viz.util convenience function to set axes limits & tick values
gvutil.set_axes_limits_and_ticks(ax1,
                                 xlim=[100, 220],
                                 ylim=[0, 1.55 * 1e16],
                                 xticks=[135, 180],
                                 yticks=np.linspace(0, 1.55 * 1e16, 7),
                                 xticklabels=['135E', '180'],
                                 yticklabels=np.arange(0, 181, 30))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax1,
                             x_minor_per_major=3,
                             y_minor_per_major=3,
                             labelsize=12)

# Use geocat.viz.util convenience function to add titles
gvutil.set_titles_and_labels(ax1,
                             maintitle="Pacific Region",
                             lefttitle="Velocity Potential",
                             righttitle="m2/s",
                             ylabel="elapsed time")

plt.show()
