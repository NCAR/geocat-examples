import shapefile as shp
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import geocat.datafiles as gdf
from geocat.viz import util as gvutil
import xarray as xr
import matplotlib.colors as colors
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from geocat.viz import util as gvutil
import matplotlib.cm as cm

colormap = colors.ListedColormap(['lightcoral', 'wheat', 'palegoldenrod', 'powderblue', 'mediumpurple',
            'indianred', 'peru', 'dodgerblue', 'slateblue', 'firebrick', 'sienna', 'olivedrab',
            'steelblue', 'navy'])

colorbounds = [0, 1, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 12, 25, 38, 40]

norm = colors.BoundaryNorm(colorbounds, colormap.N)

def getFillColor(statepopulationfile):

    nameandpopdict = {}
    Lines = statepopulationfile.read().splitlines()
    for line in Lines: 
        try:
            nameandpop = line.split(" ")
            name = nameandpop[0]
            pop = (int)(nameandpop[-1])/1000000
            nameandpopdict[name] = pop
        except:
            continue
    
    return nameandpopdict

def findDivColor(colorbounds, pdata):

    for x in range(len(colorbounds)):

        if pdata >= colorbounds[len(colorbounds)-1]:
            return colormap.colors[x-1]
        if pdata >= colorbounds[x]:
            continue
        else:
            # Index is 'x-1' because colorbounds is one item longer than colormap
            return colormap.colors[x-1]

def removeTicks(axis):

    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)

def plotRegion(shape, axis, xlim):

    for i in range(len(shape.shape.parts)):
        i_start = shape.shape.parts[i]
        if i==len(shape.shape.parts)-1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[i+1]

        x = []
        y = []
        patches = []

        for i in shape.shape.points[i_start:i_end]:
            if xlim[0] != None and i[0] < xlim[0]:
                continue
            if xlim[1] != None and i[0] > xlim[1]:
                continue
            else:
                x.append(i[0])
                y.append(i[1])

        # FILL WITH COLOR
        abbrevname = shape.record.STUSPS
        pop = nameandpopdict[abbrevname]
        color = findDivColor(colorbounds, pop)

        axis.plot(x,y, color='black', linewidth=0.3)  
        patches.append( Polygon(np.vstack((x, y)).T, True, linewidth=0.3, color=color))

        pc = PatchCollection(patches, match_original=True, edgecolor='k', linewidths=1., zorder=2)
        axis.add_collection(pc)
    
fig = plt.figure(figsize=(8, 8))
spec = gridspec.GridSpec(ncols=1, nrows=2, hspace=0.05, wspace=0.1, figure=fig, height_ratios=[2, 1])

ax1 = fig.add_subplot(spec[0, 0], frameon=False)
removeTicks(ax1)

ax2 = fig.add_subplot(spec[1, 0], frameon=False)
removeTicks(ax2)

axin1 = ax2.inset_axes([0.0, 0.4, 0.30, 0.80], frameon=False)
removeTicks(axin1)

axin2 = ax2.inset_axes([0.40, 0.4, 0.20, 0.40], frameon=False)
removeTicks(axin2)

axin3 = ax2.inset_axes([0.70, 0.4, 0.30, 0.30], frameon=False)
removeTicks(axin3)

us = shp.Reader("tl_2017_us_state\\tl_2017_us_state.dbf")

nonmainlandus = ['Commonwealth of the Northern Mariana Islands', 'Guam', 'Puerto Rico', 'Hawaii', 'Alaska', 'American Samoa', 
                 'United States Virgin Islands']  

statepopulationfile = open(gdf.get("ascii_files/us_state_population.txt"), 'r')
nameandpopdict = getFillColor(statepopulationfile)

for shape in us.shapeRecords():
    
    if shape.record.NAME not in nonmainlandus:
        plotRegion(shape, ax1, [None, None])
 
    elif shape.record.NAME == 'Alaska':
        plotRegion(shape, axin1, [None, 100])

    elif shape.record.NAME == 'Hawaii':
        plotRegion(shape, axin2, [-161, None])

    elif shape.record.NAME == 'Puerto Rico':
        plotRegion(shape, axin3, [None, None])

title = r"$\bf{Population}$"+" "+r"$\bf{in}$"+" "+r"$\bf{Millions}$"+" "+r"$\bf{(2014)}$"
gvutil.set_titles_and_labels(ax1, maintitle=title,
                             maintitlefontsize=18)

axins1 = inset_axes(ax2,
                    width="115%",
                    height="12%",
                    loc='lower center'
                    )

# Add colorbar to plot
cb = fig.colorbar(cm.ScalarMappable(cmap=colormap, norm=norm), cax=axins1, boundaries=colorbounds,
                  ticks=colorbounds[1:-1], spacing='uniform', orientation='horizontal', label='inches')

plt.show()