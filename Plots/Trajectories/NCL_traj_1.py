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
import random

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/traj_data.nc'))
sdata = ds.get('sdata')
traj = [1, 10, 53, 67, 80]
ypt = sdata[1, :, traj[1]]
xpt = sdata[2, :, traj[1]]

###############################################################################
# Define helper function to plot every fourth timestep:


def plot4thTimestep(tuparray):

    for x in range(0, len(tuparray)):
        if x == 0:
            x, y = tuparray[x]
            plt.scatter(x, y, color='green', s=4)
        if (x + 1) % 4 == 0:
            x, y = tuparray[x]
            plt.scatter(x, y, color='black', s=4)


###############################################################################
# Plot:

# Initialize axes
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-75, -30, -60, -20], crs=None)

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

random.seed(30)

# Generate random example data, trajectory 1:
traj1 = [(-30 + (random.random()*-10), -22 + (random.random()/2)) for _ in range(50)]
traj1 = sorted(traj1, key=lambda k: [-k[0]])
x1, y1 = zip(*traj1)
plt.plot(x1, y1, color='green', linewidth=0.5)
plot4thTimestep(traj1)

# Generate random example data, trajectory 2:
traj2 = [(-30 + (random.random()*-10), -23 + (random.random()/2)) for _ in range(50)]
traj2 = sorted(traj2, key=lambda k: [-k[0]])
x2, y2 = zip(*traj2)
plt.plot(x2, y2, color='red', linewidth=0.5)
plot4thTimestep(traj2)

# Generate random example data, trajectory 3:
traj3 = [(-40 + (random.random()*-8), -40 + (random.random()/2)) for _ in range(50)]
traj3 = sorted(traj3, key=lambda k: [-k[0]])
x3, y3 = zip(*traj3)
plt.plot(x3, y3, color='blue', linewidth=0.5)
plot4thTimestep(traj3)

plt.show()
