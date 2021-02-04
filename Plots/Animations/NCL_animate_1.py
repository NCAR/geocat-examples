"""
NCL_animate_1.py
===============
This script illustrates the following concepts:
   - Creating animations

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/animate_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/animate_1_1_lg.png

Please note:
    This code will create a .gif file locally. In order to view the gif, you 
    will need to right click on the .gif file in your local directory, then 
    select 'open with' then select a web browser. This has been tested using 
    Google Chrome, Safari, and Firefox. 
"""
###############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
from PIL import Image, ImageDraw

import glob
from IPython.display import display

import geocat.datafiles as gdf

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
# Disable time decoding due to missing necessary metadata
ds = xr.open_dataset(gdf.get("netcdf_files/meccatemp.cdf"), decode_times=False)

tas = ds.t

# Create empty data array
frames = []

###############################################################################
# Generate projections
for i in range(30):
       
    # Set figure size
    figsize=(10,20)
   
    # Generate axes using Cartopy and draw coastlines
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    
    # Set extent to include latitudes from 34 to 52 and longitudes from 128
    # to 144
    ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
   
    # Plot data
    tas[i,:,:].plot.contourf(
      ax=ax,
      transform=ccrs.PlateCarree(),
      vmin=195,
      vmax=328,
      levels=53,
      cmap="inferno",
      cbar_kwargs={
        "extendrect": True,
        "orientation": "horizontal",
        "ticks": np.arange(195, 332, 9),
        "label": "", "shrink":0.90})
    plt.title("January Global Surface Temperature (K) - Day  " + str(tas.coords['time'].values[i])[:13])
    plt.savefig(f"Python_Animation_frame_{i:04}.png")
    # plt.show()
    plt.close()
   
# Gather and sort the png images 
imgs = sorted(glob.glob("Python_Animation_frame_00*.png"))

# Load each png image into the empty data array in order of time
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save('png_to_gif.gif', format='GIF',
                append_images=frames[:],
                save_all=True,
                duration=300, loop=0)

# im = Image.open('Python_Animation_frame_0000.png', 'r')
im =  Image.open('png_to_gif.gif')
display(im)


