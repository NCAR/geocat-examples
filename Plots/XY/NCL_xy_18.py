"""
NCL_xy_18.py
============
Concepts illustrated:

- Filling the area between two curves in an XY plot
- Labeling the bottom X axis with years
- Drawing a main title on three separate lines
- Calculating a weighted average
- Changing the size/shape of an XY plot using viewport resources
- Manually creating a legend
- Overlaying XY plots on each other
- Maximizing plots after they've been created

See the [original NCL example](https://www.ncl.ucar.edu/Applications/Scripts/xy_18.ncl)
"""

###############################################################################
# Basic imports
import numpy as np
import xarray as xr

###############################################################################
# Open files and read in monthly data

pass
#  dir  = './'
#  v1	= addfile (dir+"TREFHT.B06.61.atm.1890-1999ANN.nc", "r")
#  v2	= addfile (dir+"TREFHT.B06.59.atm.1890-1999ANN.nc", "r")
#  v3	= addfile (dir+"TREFHT.B06.60.atm.1890-1999ANN.nc", "r")
#  v4	= addfile (dir+"TREFHT.B06.57.atm.1890-1999ANN.nc", "r")
#  n1	= addfile (dir+"TREFHT.B06.66.atm.1890-1999ANN.nc", "r")
#  n2	= addfile (dir+"TREFHT.B06.67.atm.1890-1999ANN.nc", "r")
#  n3	= addfile (dir+"TREFHT.B06.68.atm.1890-1999ANN.nc", "r")
#  n4	= addfile (dir+"TREFHT.B06.69.atm.1890-1999ANN.nc", "r")
#  g    = addfile (dir+"gw.nc","r")


###############################################################################
# Some parameters
nyrs = 110
nlon = 128
nlat = 64
time = np.linspace(1890, 1999, endpoint=True)

###############################################################################
# OBS

pass
# obs = asciiread("jones_glob_ann_2002.asc",(/146/),"float")

###############################################################################
# NATURAL
nat =
