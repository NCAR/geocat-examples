"""
NCL_sat_1.py
===============
This script illustrates the following concepts:
   - Using 'astype' to unpack 'short' data
   - Drawing line contours over a satellite map
   - Changing the view of a satellite map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/sat_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
"""

###############################################################################
# Import packages:
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"), decode_times=False)

# Get lon/lat data from the 24th timestep
U = ds.slp[24, :, :]

# Translate short values to float values
U = U.astype('float64')

# Convert Pa to hPa data
U = U*0.01

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_U = gvutil.xr_add_cyclic_longitudes(U, "lon")

###############################################################################
# Create plot

# Set figure size
fig = plt.figure(figsize=(8, 8))

# Set global axes with an orthographic projection
proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
ax = plt.axes(projection=proj)
ax.set_global()

# Add land, coastlines, and ocean features
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE, linewidth=.5)
ax.add_feature(cfeature.OCEAN, facecolor='lightcyan')
ax.add_feature(cfeature.BORDERS, linewidth=.5)
ax.add_feature(cfeature.LAKES, facecolor='lightcyan', edgecolor='k', linewidth=.5)

# Plot contour data
p = wrap_U.plot.contour(ax=ax,
                        transform=ccrs.PlateCarree(),
                        linewidths=0.5,
                        levels=30,
                        cmap='black',
                        add_labels=False)

# Specify array of contour levels to be labeled- These values were found by setting 'manual'
# argument in ax.clabel call to 'True' and then hovering mouse over desired location of
# countour label to find coordinate (which can be found in bottom left of figure window)

# low pressure contour levels- these will be plotted as a subscript to an 'L' symbol
lowClevels = [(-3.825, 4.063), (1.725, 2.026), (1.663, 4.479)]

# regular pressure contour levels
clevels = [(-4.012, 1.694), (-4.407, -1.653), (-1.206, .6752),
           (-0.9769, -3.108), (-4.989, 3.461), (1.892, .8831),
           (4.157, 0.7792), (3.118, 0.3219), (1.164, -.2601),
           (0.4781, 0.8831), (-2.972, 0.1348), (-4.344, -0.177),
           (-1.995, -2.713), (-0.1247, -2.048), (-0.4781, 4.313),
           (-0.3741, 3.128), (-1.538, -0.1354), (-0.5196, -0.9461),
           (2.661, 1.735), (4.22, -1.694), (1.455, 2.754), (1.164, -1.632),
           (1.642, -2.983), (2.827, 4.25), (4.303, 2.255),
           (0.8107, 4.271), (-0.4157, 1.756)]

# multiply each value by 10^6 to get correct window coordinates
lowClevels = [(x[0]*1000000, x[1]*1000000) for x in lowClevels]
clevels = [(x[0]*1000000, x[1]*1000000) for x in clevels]

# Label contours with Low pressure
ax.clabel(p, inline=True, fontsize=14, colors='k', fmt="L" + "$_{%.0f}$", manual=lowClevels)

# Label rest of the contours
ax.clabel(p, inline=True, fontsize=14, colors='k', fmt="%.0f", manual=clevels)

# Use gvutil function to set title and subtitles
gvutil.set_titles_and_labels(ax, maintitle=r"$\bf{SLP}$"+" "+r"$\bf{1963,}$"+" "+r"$\bf{January}$"+" "+r"$\bf{24th}$", maintitlefontsize=20,
                             lefttitle="mean Daily Sea Level Pressure", lefttitlefontsize=16, righttitle="hPa", righttitlefontsize=16)

# Set characteristics of text box
props = dict(facecolor='white', edgecolor='black', alpha=0.5)

# Place text box
ax.text(0.40, -0.1, 'CONTOUR FROM 948 TO 1064 BY 4', transform=ax.transAxes, fontsize=16, bbox=props)

# Make layout tight
plt.tight_layout()

plt.show()
