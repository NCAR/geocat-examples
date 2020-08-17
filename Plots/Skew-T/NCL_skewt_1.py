"""
NCL_skewt_1.py
===============
This script illustrates the following concepts:
   - Drawing a default Skew-T background
   - Customizing the background of a Skew-T plot
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/skewt_1.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/skewt_1_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/skewt_1_2_lg.png and https://www.ncl.ucar.edu/Applications/Images/skewt_1_3_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np
from metpy.plots import SkewT
import geocat.viz.util as gvutil

###############################################################################
# Plot Skew-T with MetPy Defaults:
## Note that there are not labels on the axes. This is because we have not yet
## plotted any data. Once data is plotted, MetPy will use the units of the
## data to create appropriate labels.
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig)

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

plt.show()
