"""
NCL_panel_18.py
===============
This script illustrates the following concepts:
   - Combining two sets of paneled plots on one page
   - Maximizing plots after they've been created
   - Assign a color palette to contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_18.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_18_lg.png
"""

##############################################################################
# Import packages:

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into
# xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/TS.cam3.toga_ENS.1950-2000.nc"),
                     decode_times=False)

##############################################################################
# Plot:
fig = plt.figure(figsize=(8, 12))

grid = gridspec.GridSpec(nrows=3, ncols=1, figure=fig)

# Choose the map projection
proj = ccrs.PlateCarree()

# Add the subplots
ax1 = fig.add_subplot(grid[0], projection=proj)  # upper cell of grid
ax2 = fig.add_subplot(grid[1], projection=proj)  # middle cell of grid
ax3 = fig.add_subplot(grid[2], projection=proj)  # lower cell of grid

for (ax, title) in [(ax1, 'Jan. 1999'), (ax2, 'Jan. 1951'),
                    (ax3, 'Difference: Jan 1999 - Jan 1951')]:
    # Use geocat.viz.util convenience function to set axes tick values
    gvutil.set_axes_limits_and_ticks(ax=ax,
                                     xlim=(-180, 180),
                                     ylim=(-90, 90),
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-90, 90, 7))

    # Use geocat.viz.util convenience function to make plots look like NCL
    # plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)

    # Remove the degree symbol from tick labels
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

    # Use geocat.viz.util convenience function to add minor and major ticks
    gvutil.add_major_minor_ticks(ax)

    # Draw coastlines
    ax.coastlines(linewidth=0.5)

    # Use geocat.viz.util convenience function to set titles
    gvutil.set_titles_and_labels(ax,
                                 lefttitle=t_1.long_name,
                                 righttitle=t_1.units,
                                 lefttitlefontsize=10,
                                 righttitlefontsize=10)
    # Add center title
    ax.set_title(title, loc='center', y=1.04, fontsize=10)

# Import NCL colormaps
newcmp = gvcmaps.BlAqGrYeOrRe
newcmp2 = gvcmaps.BlueWhiteOrangeRed

# Plot data
C = ax1.contourf(t_1['lon_t'],
                 t_1['lat_t'],
                 t_1.data,
                 levels=np.arange(0, 30, 2),
                 cmap=newcmp,
                 extend='both')
ax2.contourf(t_2['lon_t'],
             t_2['lat_t'],
             t_2.data,
             levels=np.arange(0, 30, 2),
             cmap=newcmp,
             extend='both')
C_2 = ax3.contourf(t_6['lon_t'],
                   t_6['lat_t'],
                   t_6.data,
                   levels=np.arange(0, 22, 2),
                   cmap=newcmp2,
                   extend='both')

# Add colorbars
# By specifying two axes for `ax` the colorbar will span both of them
plt.colorbar(C,
             ax=[ax1, ax2],
             ticks=range(0, 30, 2),
             extendrect=True,
             extendfrac='auto',
             shrink=0.85,
             aspect=13,
             drawedges=True)
plt.colorbar(C_2,
             ax=ax3,
             ticks=range(0, 22, 2),
             extendrect=True,
             extendfrac='auto',
             shrink=0.85,
             aspect=5.5,
             drawedges=True)

plt.show()
