"""
NCL_leg_1.py
===============
This script illustrates the following concepts:
   - Drawing a legend inside an XY plot
   - Changing the width and height of a legend
   - Turning off the perimeter around a legend
   - Changing the font size of legend labels
   - Customizing the labels in a legend

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/leg_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/leg_1_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import holoviews as hv

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

hv.extension("matplotlib")

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
# Extract variables
uz = ds.U.isel(time=0).mean(dim=['lon'])
vz = ds.V.isel(time=0).mean(dim=['lon'])

###############################################################################
# Plot:

# basic version (works with Matplotlib or Bokeh plotting)
basic = hv.Curve(vz, label="V") * hv.Curve(uz, label="U")
hv.save(basic, "/tmp/basic.png", fmt='png')

# customized Matplotlib plot
ticks = list(zip(np.linspace(-90, 90, 7), ['90S', '60S', '30S', '0', '30N', '60N', '90N']))
vc = hv.Curve(vz, label="V").opts(color="gray", linestyle='--') 
uc = hv.Curve(uz, label="U").opts(color="gray")
custom = (vc * uc).opts(xticks=ticks, show_legend=True, legend_opts=dict(loc="upper left"), fig_inches=5)
hv.save(custom, "/tmp/custom.png", fmt='png')
