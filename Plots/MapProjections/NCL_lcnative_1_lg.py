"""

NCL_lcnative_1_lg.py
================
This script illustrates the following concepts:
    - Drawing contours over a map using a native lat,lon grid
    - Drawing filled contours over a Lambert Conformal map
    - Zooming in on a particular area on a Lambert Conformal map
    - Subsetting a color map
    - Using all three Cartopy Lambert projections to find the best fit for visualization
    - Implementing best practices for choosing contour color scheme
    
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lcnative_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lcnative_1_lg.png

"""
###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geocat.datafiles as gdf
import matplotlib.ticker as mticker
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/pre.8912.mon.nc"), decode_times=False)

# Extract a slice of the data
t = ds.pre.isel(time=0)

lat2d = ds.lat[:,:]
lon2d = ds.lon[:,:]


###############################################################################
# Plot:

def Plot(proj, row, col, pos, title):

    plt.figure(figsize=(14, 14))
    # Generate axes using Cartopy and draw coastlines
    projection = proj#LambertAzimuthalEqualArea()#central_longitude=45)#, standard_parallels=(36,55), globe=ccrs.Globe())
    ax = plt.subplot(row, col, pos, projection=projection)
    ax.set_extent((28, 57, 20, 47), crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=0.5)
    
    gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    gl.xlocator = mticker.FixedLocator([30,35,40,45,50,55])
    gl.ylocator = mticker.FixedLocator([20,25,30,35,40,45])
    
    # Plot data and create colorbar
    newcmp = gvcmaps.BlueYellowRed
    t.plot.contourf(ax=ax, cmap=newcmp, transform=ccrs.PlateCarree(), levels = 14, cbar_kwargs={"orientation":"horizontal",  "ticks":np.arange(0, 240, 20),  "label":'', "shrink":0.7})
    
    plt.title(title, loc='center', size=14)
    plt.title(t.units, loc='right', size=14)
    
    plt.show()

Plot(ccrs.LambertConformal(central_longitude=45, standard_parallels=(36,55), globe=ccrs.Globe()),2,2,1,"Lambert Conformal")
Plot(ccrs.LambertCylindrical(central_longitude=45),2,2,2,"Lambert Cylindrical")
Plot(ccrs.LambertAzimuthalEqualArea(central_longitude=45),2,2,3,"Lambert Azimuthal")