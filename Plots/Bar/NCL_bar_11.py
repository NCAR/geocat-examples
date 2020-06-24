"""
NCL_bar_11.py
===============
This script illustrates the following concepts:
   - Drawing filled bars using solid colors
   - Changing the aspect ratio of a bar plot
   - Setting the minimum/maximum value of the X and Y axis in a bar plot
   - Overlaying XY plots on each other
   - Paneling bar plots  
   - Drawing a custom labelbar

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/bar_11.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/bar_11_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np

from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil


