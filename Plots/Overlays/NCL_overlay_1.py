"""
NCL_overlay_1.py
===============
This script illustrates the following concepts:
   - Overlaying line contours on filled contours
   - Explicitly setting contour levels
   - Selecting a different color map for each contour plot
   
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_1.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_1_lg.png

"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmaps
