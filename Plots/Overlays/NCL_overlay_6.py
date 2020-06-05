"""
NCL_overlay_6.py
===============
This script illustrates the following concepts:
   - Overlaying shaded contours on filled contours
   - Filling contours with multiple shaded patterns
   - Overlaying vectors on filled contours
   - Using the "palette" resources to assign a color palette to color vectors and contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_6.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_6_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

