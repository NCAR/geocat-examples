"""
NCL_traj_1.py
===============
This script illustrates the following concepts:
   - Plotting a simple trajectory plot
   - Plotting multiple trajectories in different colors
   - Plotting every nth time step in a trajectory

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/traj_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/traj_1_lg.png
"""

###############################################################################
# Import packages:
import xarray as xr
import geocat.datafiles as gdf
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/traj_data.nc'))
sdata = ds.get('sdata')


###############################################################################
# Define helper function to plot every fourth timestep:

def plot4thTimestep1(nparrayy, nparrayx):

    for x in range(0, len(nparrayx)):

        # Plot green starting point of each trajectory
        if x == 0:
            y, x = nparrayy[x], nparrayx[x]
            plt.scatter(x, y, color='green', s=4)

        # Plot every fourth timestamp
        if (x + 1) % 4 == 0:
            y, x = nparrayy[x], nparrayx[x]
            plt.scatter(x, y, color='black', s=4)


###############################################################################
# Plot:

# Initialize axes
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-75, -25, -60, -20], crs=None)

# Set title and subtitle
plt.suptitle('Example of a Trajectory Plot')
plt.title('markers every 4th timestep', fontsize=10, pad=10)

# Set land feature
ax.add_feature(cfeature.LAND, color='grey')

# Set formatted axes ticks (with degree symbol and direction)
formatterW = ticker.EngFormatter(unit=u'\N{DEGREE SIGN}'+'W')
formatterS = ticker.EngFormatter(unit=u'\N{DEGREE SIGN}'+'S')

# Set ticks on x axis
ax.set_xticks([-70, -60, -50, -40, -30], minor=False, crs=None)
ax.xaxis.set_major_formatter(formatterW)

# Set ticks on y axis
ax.set_yticks([-60, -50, -40, -30, -20], minor=False, crs=None)
ax.yaxis.set_major_formatter(formatterS)

# Select trajectories to plot
traj = [1, 10, 53, 67, 80]

# Set colors of each trajectory line
trajlinecolors = ["red", "blue", "green", "grey", "magenta"]

# Plot each trajectory
for i in range(len(traj)):

    # Extract latitude
    ypt = (np.array(sdata[1, :, traj[i]])-360)

    # Extract longitude
    xpt = np.array(sdata[2, :, traj[i]])

    plt.plot(ypt, xpt, color=trajlinecolors[i], linewidth=0.5)

    plot4thTimestep1(xpt, ypt)

plt.show()
