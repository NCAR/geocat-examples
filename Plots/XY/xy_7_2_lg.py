"""
xy_7_2_lg.py
===============
An example of a double y plot: two separate line with their own unique axis.

- Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/xy_7.ncl
- https://www.ncl.ucar.edu/Applications/Images/xy_7_2_lg.png

"""

###############################################################################
# Import modules
# ===============

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import geocat.datafiles

################################################################################
# Open data file and extract a slice of the data
# ===============================================

dset = xr.open_dataset(geocat.datafiles.get("netcdf_files/TestData.xy3.nc"))
ds = dset.isel(case=0, time=slice(0, 36))


################################################################################
# Create XY plot with two different Y axes
# =========================================


def nclize_axis(ax):
    """
    Utility function to make plots look like NCL plots
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=1.5,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=5,
        width=0.75,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )


fig, ax1 = plt.subplots(figsize=(12, 8))
nclize_axis(ax1)
ax1.set_xlabel(ds.time.long_name, fontsize=24)
ax1.set_ylabel(f"{ds.T.long_name} [solid]", fontsize=24)
ax1.plot(ds.time, ds.T, color="blue", linestyle="-", linewidth=2.0)
ax1.tick_params(axis="both", labelsize=20)
ax1.set_xlim(xmin=1970, xmax=1973)
ax1.set_ylim(ymin=0.0, ymax=16.0)
ax1.set_yticks(np.arange(0, 17, 3))


ax2 = ax1.twinx()
nclize_axis(ax2)


# we already handled the x-label with ax1

ax2.set_ylabel(f"{ds.P.long_name} [dash]", fontsize=24)
ax2.plot(ds.time, ds.P, color="red", linestyle="--", linewidth=2.0, dashes=[6.5, 3.7])
ax2.tick_params(axis="both", labelsize=20)
ax2.set_ylim(ymin=1008, ymax=1024.0)
ax2.set_yticks(np.arange(1008, 1025, 3))


plt.title("Curves Offset", fontsize=24, fontweight="bold", y=1.05)

fig.tight_layout()
plt.show()
