"""
NCL_xy_3.py
===============
   - Reversing the Y axis
   - Changing the line dash pattern in an XY plot
   - Creating your own line dash pattern for an XY plot
   - Changing the line color and thickness in an XY plot
   - Creating a vertical profile plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_3.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/xy_3_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/xy_3_2_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
