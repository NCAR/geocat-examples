"""
NCL_panel_6.py
===============
This script illustrates the following concepts:
   - Paneling four plots on a page
   - Adding white space around paneled plots

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_6.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_6_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/panel_6_2_lg.png
Note:
    A different colormap was used in this example than in the NCL example
    because rainbow colormaps do not translate well to black and white formats,
    are not accessible for individuals affected by color blindness, and
    vary widely in how they are percieved by different people. See this
    `example <https://geocat-examples.readthedocs.io/en/latest/gallery/Colors/CB_Temperature.html#sphx-glr-gallery-colors-cb-temperature-py>`_
    for more information on choosing colormaps.
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.contour as mcontour
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz.util as gvutil

###############################################################################


# Define a helper function to draw the map boundary
def set_map_boundary(ax, lon_range, lat_range, north_pad=0, south_pad=0, east_pad=0, west_pad=0, res=1):
    """
    Utility function to set the boundary of ax to a path that surrounds a
    given region specified by latitude and longitude coordinates. This
    boundary is drawn in the projection coordinates and therefore follows
    any curves created by the projection. As of now, this only works
    consistently for the Lambert Conformal Projection and North/South
    Polar Stereographic Projections.
    Note: Due to the behavior of cartopy's set_extent() function, the curved
    edges of the boundary may be flattened and cut off. To solve this, use the
    kwargs north_pad, south_pad, east_pad, and west_pad. These will modify the
    coordinates passed to set_extent(). For the Lambert Conformal and Polar
    Stereographic projections, typically only north_pad and south_pad are
    needed. If attempting to use this function for other projections
    (i.e. Othographic) east_pad and west_pad may be needed.
    Args:
        ax (:class:`matplotlib.axes`):
            The axes to which the boundary will be applied.

        lon_range (:class:`tuple` or :class:`list`):
            The two-tuple containing the start and end of the desired range of
            longitudes. The first entry must be smaller than the second entry,
            except when the region crosses the antimeridian. Both entries must
            be between [-180 , 180]. If lon_range is from -180 to 180, then a
            full circle centered on the pole with a radius from the pole to the
            lowest latitude given by lat_range will be set as the boundary.

        lat_range (:class:`tuple` or :class:`list`):
            The two-tuple containing the start and end of the desired range of
            latitudes. The first entry must be smaller than the second entry.
            Both entries must be between [-90 , 90].

        north_pad (:class:`int`):
            A constant to be added to the second entry in lat_range. Use this
            if the northern edge of the plot is cut off. Defaults to 0.

        south_pad (:class:`int`);
            A constant to be subtracted from the first entry in lat_range. Use
            this if the southern edge of the plot is cut off. Defaults to 0.

        east_pad (:class:`int`):
            A constant to be added to the second entry in lon_range. Use this
            if the eastern edge of the plot is cut off. Defaults to 0.

        west_pad (:class:`int`):
            A constant to be subtracted from the first entry in lon_range. Use
            this if the western edge of the plot is cut off. Defaults to 0.
        res (:class:`int`):
            The size of the incrementation for vertices in degrees. Default is
            a vertex every one degree of longitude. A higher number results in
            a lower resolution boundary.
    """
    import cartopy.crs as ccrs
    import matplotlib.path as mpath

    if (lon_range[0] >= lon_range[1]):
        if not (lon_range[0] > 0 and lon_range[1] < 0):
            raise ValueError("The first longitude value must be strictly less \
                              than the second longitude value unless the \
                              region crosses over the antimeridian")

    if (lat_range[0] >= lat_range[1]):
        raise ValueError("The first latitude value must be strictly less than \
                          the second latitude value")

    if (lon_range[0] > 180 or lon_range[0] < -180 or lon_range[1] > 180 or lon_range[1] < -180):
        raise ValueError("The longitudes must be within the range [-180, 180] inclusive")

    if (lat_range[0] > 90 or lat_range[0] < -90 or lat_range[1] > 90 or lat_range[1] < -90):
        raise ValueError("The latitudes must be within the range [-90, 90] inclusive")

    # Make a boundary path in PlateCarree projection beginning in the south
    # west and continuing anticlockwise creating a point every `res` degree
    if (lon_range[0] >= 0 and lon_range[1] <= 0):  # Case when range crosses antimeridian
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], 180 + 1, res)] + \
                   [(lon, lat_range[0]) for lon in range(-180, lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], -180 - 1, -res)] + \
                   [(lon, lat_range[1]) for lon in range(180, lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat) for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)
    elif ((lon_range[0] == 180 or lon_range[0] == -180) and (lon_range[1] == 180 or lon_range[1] == -180)):
        verts = [(lon, lat_range[0]) for lon in range(0, 360 + 1, res)]
        path = mpath.Path(verts)
    else:
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat) for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)

    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
    ax.set_boundary(proj_to_data.transform_path(path))

    ax.set_extent([lon_range[0] - west_pad, lon_range[1] + east_pad,
                  lat_range[0] - south_pad, lat_range[1] + north_pad],
                  crs=ccrs.PlateCarree())


###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/h_avg_Y0191_D000.00.nc"), decode_times=False)

data0 = ds.T.isel(time=0, drop=True).isel(z_t=0, drop=True)
data1 = ds.T.isel(time=0, drop=True).isel(z_t=5, drop=True)
data2 = ds.S.isel(time=0, drop=True).isel(z_t=0, drop=True)
data3 = ds.S.isel(time=0, drop=True).isel(z_t=3, drop=True)

data0 = gvutil.xr_add_cyclic_longitudes(data0, "lon_t")
data1 = gvutil.xr_add_cyclic_longitudes(data1, "lon_t")
data2 = gvutil.xr_add_cyclic_longitudes(data2, "lon_t")
data3 = gvutil.xr_add_cyclic_longitudes(data3, "lon_t")

data = [[data0, data1], [data2, data3]]

###############################################################################
# Plot without extra whitespace:
projection = ccrs.NorthPolarStereo()
fig, axs = plt.subplots(2, 2, figsize=(8, 8),
                        subplot_kw=dict(projection=projection))

# Format axes and inset axes for color bars
cax = np.empty((2, 2), dtype=plt.Axes)
for row in range(0, 2):
    for col in range(0, 2):
        # Add map features
        axs[row][col].add_feature(cfeature.LAND, facecolor='silver', zorder=2)
        axs[row][col].add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
        axs[row][col].add_feature(cfeature.LAKES, linewidth=0.5,
                                  edgecolor='black', facecolor='None',
                                  zorder=4)

        # Add gridlines
        gl = axs[row][col].gridlines(ccrs.PlateCarree(), draw_labels=False,
                                     color='gray', linestyle="--", zorder=5)
        gl.xlocator = mticker.FixedLocator(np.linspace(-180, 150, 12))

        # Add latitude and longitude labels
        x = np.arange(0, 360, 30)
        # Array specifying 8S, this makes an offset from the circle boundary
        # which lies at the equator
        y = np.full_like(x, -8)
        labels = ['0', '30E', '60E', '90E', '120E', '150E', '180',
                  '150W', '120W', '90W', '60W', '30W']
        for x, y, label in zip(x, y, labels):
            if label == '180':
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='top',
                                   transform=ccrs.Geodetic())
            elif label == '0':
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='bottom',
                                   transform=ccrs.Geodetic())
            else:
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='center',
                                   transform=ccrs.Geodetic())

        # Set boundary of plot to be circular
        set_map_boundary(axs[row][col], (-180, 180), (0, 90))
        # Create inset axes for color bars
        cax[row][col] = inset_axes(axs[row][col], width='5%', height='100%',
                                   loc='lower right',
                                   bbox_to_anchor=(0.175, 0, 1, 1),
                                   bbox_transform=axs[row][col].transAxes,
                                   borderpad=0)
# Import color map
cmap = "magma"

# Plot filled contours
contour = np.empty((2, 2), dtype=mcontour.ContourSet)
contour[0][0] = data[0][0].plot.contourf(ax=axs[0][0],
                                         cmap=cmap,
                                         levels=np.arange(-2, 34, 2),
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[0][1] = data[0][1].plot.contourf(ax=axs[0][1],
                                         cmap=cmap,
                                         levels=np.arange(-4, 30, 2),
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[1][0] = data[1][0].plot.contourf(ax=axs[1][0],
                                         cmap=cmap,
                                         levels=15,
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[1][1] = data[1][1].plot.contourf(ax=axs[1][1],
                                         cmap=cmap,
                                         levels=12,
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)

# Plot contour lines
data[0][0].plot.contour(ax=axs[0][0],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=np.arange(-2, 34, 2),
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[0][1].plot.contour(ax=axs[0][1],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=np.arange(-4, 30, 2),
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[1][0].plot.contour(ax=axs[1][0],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=15,
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[1][1].plot.contour(ax=axs[1][1],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=12,
                        transform=ccrs.PlateCarree(),
                        zorder=1)

# Create colorbars and reduce the font size
for row in range(0, 2):
    for col in range(0, 2):
        cbar = plt.colorbar(contour[row][col], cax=cax[row][col])
        cbar.ax.tick_params(labelsize=7)

# Format titles for each subplot
for row in range(0, 2):
    for col in range(0, 2):
        axs[row][col].set_title(data[row][col].long_name, loc='left',
                                fontsize=7, pad=20)
        axs[row][col].set_title(data[row][col].units, loc='right',
                                fontsize=7, pad=20)

plt.show()

###############################################################################
# Plot with extra whitespace:
#
# The keyword argument ``gridspec_kw`` accepts a dictionary with keywords passed
# to the GridSpec constructor used to create the grid the subplots are placed
# on. See the documentation for `GridSpec <https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.gridspec.GridSpec.html#matplotlib.gridspec.GridSpec>`_
# for more information on how to manipulate the gridlayout.

projection = ccrs.NorthPolarStereo()
fig, axs = plt.subplots(2, 2, figsize=(8, 8), gridspec_kw=(dict(wspace=0.5)),
                        subplot_kw=dict(projection=projection))
#
# Everything beyond this is the same code for the example without extra white space
#

# Format axes and inset axes for color bars
cax = np.empty((2, 2), dtype=plt.Axes)
for row in range(0, 2):
    for col in range(0, 2):
        # Add map features
        axs[row][col].add_feature(cfeature.LAND, facecolor='silver', zorder=2)
        axs[row][col].add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
        axs[row][col].add_feature(cfeature.LAKES, linewidth=0.5,
                                  edgecolor='black', facecolor='None',
                                  zorder=4)

        # Add gridlines
        gl = axs[row][col].gridlines(ccrs.PlateCarree(), draw_labels=False,
                                     color='gray', linestyle="--", zorder=5)
        gl.xlocator = mticker.FixedLocator(np.linspace(-180, 150, 12))

        # Add latitude and longitude labels
        x = np.arange(0, 360, 30)
        # Array specifying 8S, this makes an offset from the circle boundary
        # which lies at the equator
        y = np.full_like(x, -8)
        labels = ['0', '30E', '60E', '90E', '120E', '150E', '180',
                  '150W', '120W', '90W', '60W', '30W']
        for x, y, label in zip(x, y, labels):
            if label == '180':
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='top',
                                   transform=ccrs.Geodetic())
            elif label == '0':
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='bottom',
                                   transform=ccrs.Geodetic())
            else:
                axs[row][col].text(x, y, label, fontsize=7,
                                   horizontalalignment='center',
                                   verticalalignment='center',
                                   transform=ccrs.Geodetic())

        # Set boundary of plot to be circular
        set_map_boundary(axs[row][col], (-180, 180), (0, 90))
        # Create inset axes for color bars
        cax[row][col] = inset_axes(axs[row][col], width='5%', height='100%',
                                   loc='lower right',
                                   bbox_to_anchor=(0.175, 0, 1, 1),
                                   bbox_transform=axs[row][col].transAxes,
                                   borderpad=0)
# Import color map
cmap = "magma"

# Plot filled contours
contour = np.empty((2, 2), dtype=mcontour.ContourSet)
contour[0][0] = data[0][0].plot.contourf(ax=axs[0][0],
                                         cmap=cmap,
                                         levels=np.arange(-2, 34, 2),
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[0][1] = data[0][1].plot.contourf(ax=axs[0][1],
                                         cmap=cmap,
                                         levels=np.arange(-4, 30, 2),
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[1][0] = data[1][0].plot.contourf(ax=axs[1][0],
                                         cmap=cmap,
                                         levels=15,
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)
contour[1][1] = data[1][1].plot.contourf(ax=axs[1][1],
                                         cmap=cmap,
                                         levels=12,
                                         transform=ccrs.PlateCarree(),
                                         add_colorbar=False,
                                         zorder=0)

# Plot contour lines
data[0][0].plot.contour(ax=axs[0][0],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=np.arange(-2, 34, 2),
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[0][1].plot.contour(ax=axs[0][1],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=np.arange(-4, 30, 2),
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[1][0].plot.contour(ax=axs[1][0],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=15,
                        transform=ccrs.PlateCarree(),
                        zorder=1)
data[1][1].plot.contour(ax=axs[1][1],
                        colors='black',
                        linestyles='solid',
                        linewidths=0.5,
                        levels=12,
                        transform=ccrs.PlateCarree(),
                        zorder=1)

# Create colorbars and reduce the font size
for row in range(0, 2):
    for col in range(0, 2):
        cbar = plt.colorbar(contour[row][col], cax=cax[row][col])
        cbar.ax.tick_params(labelsize=7)

# Format titles for each subplot
for row in range(0, 2):
    for col in range(0, 2):
        axs[row][col].set_title(data[row][col].long_name, loc='left',
                                fontsize=7, pad=20)
        axs[row][col].set_title(data[row][col].units, loc='right',
                                fontsize=7, pad=20)

plt.show()
