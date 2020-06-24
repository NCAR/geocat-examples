
###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
plt.figure()

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-125,-60,15,65], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, color='lightgrey')
#ax.add_feature(cfeature.LAKES, color='white')

plt.plot([-120, -64], [20, 60],'-', color='blue',  transform=ccrs.Geodetic())

x1=np.linspace(-120,-64, 5)


#Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

#Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, labelsize=12)

#Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, lefttitle='Anomalies: Surface Temperature', righttitle='K')