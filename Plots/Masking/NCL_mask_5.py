###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import matplotlib.patches as mpatches

from geocat.viz import util as gvutil
import geocat.datafiles as gdf
###############################################################################
# Plot
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)
t = ds.TS.isel(time=0)

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_t = gvutil.xr_add_cyclic_longitudes(t, "lon")
                    
###############################################################################
#Plot:

fig = plt.figure(figsize=(14, 14))

def Plot(row, col, pos, title):
    """
    Helper function to create two similar plots where subplot position
    and title can all be customized on the same style
    map projection.
    
    Args:
        
        row (:class: 'int'): 
            number of rows necessary for subplotting of visualizations
        col (:class: 'int'): 
            number of columns necessary for subplotting 
        pos (:class: 'int'): 
            position of visualization in m x n subplot
        title (:class: 'str'): 
            title of graph in format "Title"
     """
    
    # Generate axes, using Cartopy, drawing coastlines, and adding features
    projection = ccrs.PlateCarree()
    ax = plt.subplot(row, col, pos, projection=projection)
    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, color="green")
    ax.add_feature(cfeature.LAKES, color="plum")
    ax.add_feature(cfeature.OCEAN, color="blue")

    # Create label names and define colors for the legend
    land = mpatches.Rectangle((0, 0), 1, 1, facecolor="green")
    lakes = mpatches.Rectangle((0, 0), 1, 1, facecolor="plum")
    ocean = mpatches.Rectangle((0, 0), 1, 1, facecolor="blue")
    
    labels = ['Land ', 'Lakes', 'Ocean']
    
    plt.legend([land, lakes, ocean], labels,
               loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
        
    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax,
        maintitle=title,
        maintitlefontsize=12)

# #Plot first color map
Plot(2, 2, 1, "land sea mask using 'atmos.nc'")


def Plot2(row, col, pos, title):

    """
    Helper function to create two similar plots where subplot position
    and title can all be customized on the same style
    map projection.
    
    Args:
        
        row (:class: 'int'): 
            number of rows necessary for subplotting of visualizations
        col (:class: 'int'): 
            number of columns necessary for subplotting 
        pos (:class: 'int'): 
            position of visualization in m x n subplot
        title (:class: 'str'): 
            title of graph in format "Title"
     """
   
    ax1 = plt.subplot(row, col, pos, projection=ccrs.PlateCarree())
    ax1.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
    ax1.coastlines(linewidths=0.5)

    plt.suptitle(title, x=0.3, y=.45, fontsize=12)

    # Import an NCL colormap
    newcmp = 'magma' 
    
    # Contourf-plot data
    wrap_t.plot.contourf(ax=ax1, transform=ccrs.PlateCarree(),
                    vmin = 230, vmax = 320, levels = 18, cmap = newcmp,
                    cbar_kwargs={"orientation":"horizontal", "extendrect":True, "label": "",
                                 "ticks":np.linspace(230, 320, 18)})
    
    ax1.add_feature(cfeature.OCEAN, zorder=10, edgecolor='k')
 
    
    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
        # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax1,
        maintitle="",
        maintitlefontsize=14,
        righttitle="degK",
        righttitlefontsize=12,
        lefttitle="temperature",
        lefttitlefontsize=12)
    
Plot2(2, 2, 3, "dummy TS field (ocean-masked)")