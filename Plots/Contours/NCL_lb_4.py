"""
NCL_lb_4.py
===============
This script illustrates the following concepts:
   - Drawing a horizontal colorbar
   - Changing the labelbar labels
   - Adding a title to a labelbar
   - Changing the font of the labelbar's labels
   - Making the labelbar label fonts smaller
   - Centering the labels inside each box in a labelbar
   - Adding a vertical title to a labelbar

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lb_4.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lb_4_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

