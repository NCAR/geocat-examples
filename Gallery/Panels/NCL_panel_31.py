"""
NCL_panel_31.py
===============
This script illustrates the following concepts:
   - Paneling 8 plots on a page
   - Adding a common title to paneled plots
   - Overlaying an image onto a map
   - Adding a vector field to a map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_31.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_31_lg.png
"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr

import geocat.viz as gv
import geocat.datafiles as gdf

###############################################################################
# Read in Data:

# Read in the image file
fname = 'EarthMap.jpg'
img = plt.imread(fname)

# Read in the vector data using xarray
ds = xr.open_dataset(gdf.get("netcdf_files/uvt.nc")).isel(time=0)

# Select zonal and meridional wind
U = ds.U
V = ds.V

# Select latitude and longitudes
lat = ds.lat
lon = ds.lon

###############################################################################
# Convenience function
# Since we will repeat this code many times, use a convenience function to
# plot the image on the map


def plot_img(ax):
    """Plot the image on the map for the given axes."""
    img_extent = (-180, 180, -90, 90)

    # Set extent of the map
    ax.set_extent([65, 95, 5, 25])

    # add the image. The "origin" of the image is in the upper left corner
    ax.imshow(img,
              origin='upper',
              extent=img_extent,
              transform=ccrs.PlateCarree())
    ax.coastlines(resolution='50m', color='black', linewidth=1)

    # Add vectors onto the plot
    Q = plt.quiver(lon,
                   lat,
                   U.sel(lev=1000),
                   V.sel(lev=1000),
                   color='white',
                   pivot='middle',
                   width=.0025,
                   scale=75)

    # Use geocat-viz utility function to format lat/lon tick labels
    gv.add_lat_lon_ticklabels(ax=ax)

    # Use geocat-viz utility function to customize tick marks
    gv.set_axes_limits_and_ticks(ax,
                                 xlim=(65, 95),
                                 ylim=(5, 25),
                                 xticks=range(65, 100, 5),
                                 yticks=range(5, 27, 5))


###############################################################################
# Plot:

# Create a figure and axes
fig, axs = plt.subplots(ncols=2, nrows=4, figsize=(8, 16))

# Define pressures
pressure = [1000, 850, 700, 500, 400, 300, 250, 200]

# Set image extent
img_extent = (-180, 180, -90, 90)

# Loop through each axes and plot
# Loop through each row
for i in range(4):
    # Loop through each column
    for j in range(2):
        # Set axes
        ax = axs[i][j]

        # Set extent of the map
        ax.set_extent([65, 95, 5, 25])

        # add the image. The "origin" of the image is in the upper left corner
        ax.imshow(img,
                  origin='upper',
                  extent=img_extent,
                  transform=ccrs.PlateCarree())
        ax.coastlines(resolution='50m', color='black', linewidth=1)

        # Add vectors onto the plot
        Q = plt.quiver(lon,
                       lat,
                       U.sel(lev=pressure[i]),
                       V.sel(lev=pressure[i]),
                       color='white',
                       pivot='middle',
                       width=.0025,
                       scale=75)

        # Use geocat-viz utility function to format lat/lon tick labels
        gv.add_lat_lon_ticklabels(ax=ax)

        # Use geocat-viz utility function to customize tick marks
        gv.set_axes_limits_and_ticks(ax,
                                     xlim=(65, 95),
                                     ylim=(5, 25),
                                     xticks=range(65, 100, 5),
                                     yticks=range(5, 27, 5))

        # Customize tick labels
        ax.tick_params(labelsize=12, length=8)

#####

# fig = plt.figure(figsize=(8, 12))

# ax = plt.axes(projection=ccrs.PlateCarree())

# # Set extent of the map
# ax.set_extent([65, 95, 5, 25])

# # add the image. The "origin" of the image is in the upper left corner
# ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())
# ax.coastlines(resolution='50m', color='black', linewidth=1)

# # Add vectors onto the plot
# Q = plt.quiver(lon, lat, U.sel(lev=1000), V.sel(lev=1000), color='white', pivot='middle', width=.0025, scale=75)

# # Use geocat-viz utility function to format lat/lon tick labels
# gv.add_lat_lon_ticklabels(ax=ax)

# # Use geocat-viz utility function to customize tick marks
# gv.set_axes_limits_and_ticks(ax,
#                              xlim=(65, 95),
#                              ylim=(5, 25),
#                              xticks=range(65, 100, 5),
#                              yticks=range(5, 27, 5))

# # Customize tick labels
# ax.tick_params(labelsize=12, length=8)

# plt.show()
