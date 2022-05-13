"""
NCL_color_1.py
===============
This script illustrates the following concepts:
   - Recreating a default NCL colormap
   - Using Geocat-Viz Contour

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/color_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/color_1_lg.png

Note:
    This may not be the best colormap to interpret the information, but was included here in order to
    demonstrate how to recreate the original NCL colormap. For more information on colormap choices, see the
    Colors examples in the GeoCAT-examples documentation.
"""

###############################################################################
# Import packages:

import matplotlib.pyplot as plt
import xarray as xr
import cmaps

import geocat.viz as gv
import geocat.datafiles as gdf

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarray
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)

###############################################################################
# Plot with geocat.viz

fig = plt.figure(figsize=(12, 8))

gv.Contour(ds.U,
           main_title="Default Color",
           fig=fig,
           other=fig,
           cmap=cmaps.ncl_default)

plt.show()
