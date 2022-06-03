"""
NCL_coneff_8.py
================
This script illustrates the following concepts:
   - Showing features of the new color display model
   - Using a NCL colormap with levels to assign a color palette to contours
   - Drawing partially transparent filled contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/coneff_8.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/coneff_8_lg.png
"""

###############################################################################
# Import Packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import geocat.datafiles as gdf
import geocat.viz as gv
from geocat.comp import interp_hybrid_to_pressure
###############################################################################
# Read in Data

# Open a netCDF data file using xarray default engine and load the data into an xarray
ds = xr.open_dataset(gdf.get('netcdf_files/atmos.nc'), decode_times=False)

## Select zonal wind
u = ds.U.isel(time=0)

## Define inputs for geocat-comp interpolation function
hyam = ds.hyam  # hybrid A coefficient
hybm = ds.hybm  # hybrid B coefficient
ps = ds.PS.isel(time=0)  # surface pressures in Pascals
p0 = 100000  # surface reference pressure in Pascals

## Specify output pressure levels in millibars
new_levels = np.array([1000, 850, 700, 500, 400, 300, 250, 200])
new_levels = new_levels * 100  # convert to Pascals

# Interpolate pressure coordinates from hybrid sigma coord
u_int = interp_hybrid_to_pressure(u,
                                  ps,
                                  hyam,
                                  hybm,
                                  p0=p0,
                                  new_levels=new_levels,
                                  method='log')
# Calculate zonal mean
uzon = u_int.mean(dim='lon')

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
plt.figure(figsize=(7, 7))
ax1 = plt.gca()
ax1.invert_yaxis()
ax2 = ax1.twinx()

# Format log axis
plt.yscale('log')
ax1.yaxis.set_major_formatter(ScalarFormatter())

# Plot filled contours ADD CMAP HERE!!
levels = np.arange(0, 24, 8)
p = uzon.plot.contourf(ax=ax1,
                       levels=levels,
                       vmin=0,
                       vmax=25,
                       add_colorbar=False,
                       add_labels=False)

# Plot contour lines
uzon.plot.contour(ax=ax1,
                  levels=12,
                  vmin=-8,
                  vmax=40,
                  colors='black',
                  linewidths=0.5,
                  linestyles='solid',
                  add_labels=False)

# Label the contours
ax1.clabel(
    p,
    levels=levels,
    fontsize=8,
    fmt="%.0f",  # Turn off decimal points
)

# Use geocat-viz utility function to configure labels
gv.set_titles_and_labels(ax1, lefttitle="Zonal Wind", lefttitlefontsize=16)

# Label left and right y-axis
ax1.set_ylabel("Pressure (mb)", fontsize=20)
ax2.set_ylabel("Height (km)", fontsize=20)

# Format x-axis to show latitudes
lat_formatter = LatitudeFormatter(degree_symbol='')
ax1.xaxis.set_major_formatter(lat_formatter)

# Use geocat-viz utility function to add minor ticks on x-axis for both axes
gv.add_major_minor_ticks(ax1,
                         x_minor_per_major=3,
                         y_minor_per_major=1,
                         labelsize=12)

gv.add_major_minor_ticks(ax2,
                         x_minor_per_major=3,
                         y_minor_per_major=1,
                         labelsize=12)

# Use geocat-viz utility function to configure tick labels
gv.set_axes_limits_and_ticks(ax1,
                             xlim=None,
                             ylim=(100000, 20000),
                             xticks=np.linspace(-60, 60, 5),
                             yticks=np.flip(new_levels),
                             xticklabels=None,
                             yticklabels=np.flip(
                                 (new_levels / 100).astype(int)))
