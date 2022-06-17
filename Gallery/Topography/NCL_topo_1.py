"""
NCL_topo_1.py
===============
This script illustrates the following concepts:
   - Drawing a topographic map using 1' data
   - Drawing topographic data using the default NCL color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/topo_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/topo_1_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.viz as gv

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset('~/Downloads/colorado.nc')

# Select Band2
ds = ds.Band2

###############################################################################
# Plot

# Generate figure and set size
plt.figure(figsize=(10, 7))

# Generate axes, using Cartopy
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)

ax.coastlines(zorder=10)

# Set map extent [lonmin, lonmax, latmin, latmax]
ax.set_extent([-120, -92, 30, 50])

states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

ax.add_feature(states_provinces, edgecolor='black')

ds.plot(ax=ax, transform=projection, cmap='terrain', add_colorbar=False)
