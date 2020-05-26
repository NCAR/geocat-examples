#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:38:46 2020

@author: misi1684
"""
import numpy as np
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import geocat.datafiles as gdf
import matplotlib.ticker as mticker
from geocat.viz import util as gvutil

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
U=ds.U[1,:,:]

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
wrap_U = gvutil.xr_add_cyclic_longitudes(U, "lon")

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10,10))

# Generate axes, using Cartopy, drawing coastlines, and adding features
fig = plt.figure(figsize=(10,10))
projection = ccrs.NorthPolarStereo()
ax = plt.axes(projection=projection)
ax.coastlines(linewidths=0.5)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Set extent to include latitudes between 0 and 40 and longitudes between -180 and 180 only
ax.set_extent([-180,180,0,40], ccrs.PlateCarree())

# Set draw_labels to False so that you can manually manipulate it later
gl = ax.gridlines(ccrs.PlateCarree(), draw_labels=False, linestyle="--", color='k')

# Manipulate latitude and longitude gridline numbers and spacing
gl.ylocator = mticker.FixedLocator(np.arange(0, 90, 15))
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))

# Set boundary to a circle
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# Manipulate longitude labels (0, 30 E, 60 E, ..., 30 W, etc.)
ticks = np.arange(0, 210, 30)
etick = ['0'] + ['%d$^\circ$E' % tick for tick in ticks if (tick != 0) & (tick != 180)] + ['180']
wtick = ['%d$^\circ$W' % tick for tick in ticks if (tick != 0) & (tick != 180)]
labels = etick + wtick
xticks = [-0.8, 28, 58, 89.1, 120, 151, 182.9, -36, -63, -89, -114, -140]
yticks = [-3] + [-2] + [-1] + [-1] * 2 + [-1] + [-3] + [-7] + [-7] * 3 + [-7]




for xtick, ytick, label in zip(xticks, yticks, labels):
    ax.text(xtick, ytick, label, transform=ccrs.Geodetic())


# Contour-plot U-data
p = wrap_U.plot.contour(ax=ax,vmin=-8,vmax=16, transform=ccrs.PlateCarree(),
                    levels = np.arange(-12,44,4), linewidths=0.5, cmap='k', add_labels=False)

ax.clabel(p, np.arange(-8,17,8),fmt='%d', inline=1, fontsize=14)

# # Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax, lefttitle="Zonal Wind", righttitle="m/s")
                            
# Add lower text box
ax.text(1.0, -.10, "CONTOUR FROM -12 TO 40 BY 4",
        fontname='Helvetica',
        horizontalalignment='right',
        transform=ax.transAxes,
        bbox=dict(boxstyle='square, pad=0.25', facecolor='white', edgecolor='black'))

# Show the plot
plt.show()
