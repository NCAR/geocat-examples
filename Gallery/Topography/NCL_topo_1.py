"""
NCL_topo_1.py
===============
This script illustrates the following concepts:
   - Drawing a topographic map using 1' data
   - Drawing topographic data using the default NCL color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/topo_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/topo_1_lg.png
"""

###############################################################################
# Import packages:
import xarray as xr

###############################################################################
# Read in data:
