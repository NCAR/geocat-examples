"""
NCL_stream_9.py
===============
This script illustrates the following concepts:
   - Showing features of the new color display model
   - Using opacity to emphasize or subdue overlain features
   - Using stLevelPalette resource to assign a color palette

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/stream_9.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/stream_9_1_lg.png

"""

################################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.cm as cm
import geocat.datafiles as gdf
from geocat.viz import util as gvutil
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
################################################################################
# Make color map 

colormap = colors.ListedColormap(['darkblue', 'mediumblue', 'blue', 'cornflowerblue', 'skyblue', 'aquamarine',
        'lime', 'greenyellow', 'gold', 'orange', 'orangered', 'red', 'maroon'])

colorbounds = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]

norm = colors.BoundaryNorm(colorbounds, colormap.N)
################################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds1 = xr.open_dataset(gdf.get('netcdf_files/U500storm.cdf'))
ds2 = xr.open_dataset(gdf.get('netcdf_files/V500storm.cdf'))

################################################################################
fig = plt.figure(figsize=(10, 8))

#proj = ccrs.LambertAzimuthalEqualArea(central_longitude=-100, central_latitude=40)
ax = fig.add_axes([.1,.2,.8,.6], projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-100, central_latitude=40), frameon=False)

# Set axis projection
#ax = plt.axes(projection=proj)
# Set extent to include roughly the United States
ax.set_extent((-128, -58, 18, 65), crs=ccrs.PlateCarree())
ax.add_feature(cfeature.OCEAN, color='lightblue')
ax.add_feature(cfeature.LAKES, color='white', edgecolor='black')
ax.add_feature(cfeature.LAND, color='tan')
ax.coastlines()

# Extract a 2D horizontal slice from the first time step of the 3D U and V variables at the bottom level
U = ds1.u.isel(timestep=0)
V = ds2.v.isel(timestep=0)
streams = ax.streamplot(U.lon, U.lat, U.data, V.data, transform=ccrs.PlateCarree(), arrowstyle='->', linewidth=1, density=2.2, color=norm(U))

ax2 = fig.add_axes([.1,.1,.8,.05])

cb = fig.colorbar(cm.ScalarMappable(cmap=colormap, norm=norm), cax=ax2, boundaries=colorbounds,
                  ticks=colorbounds, spacing='uniform', orientation='horizontal', label='inches')

plt.show()