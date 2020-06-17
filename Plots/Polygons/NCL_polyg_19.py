import shapefile as shp
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

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

        axis.plot(x,y, color='black', linewidth=0.3)  
        patches.append( Polygon(np.vstack((x, y)).T, True, linewidth=0.3, color='lightgray') )

        pc = PatchCollection(patches, match_original=True, edgecolor='k', linewidths=1., zorder=2)
        axis.add_collection(pc)

fig = plt.figure(figsize=(5, 6))
spec = gridspec.GridSpec(ncols=1, nrows=2, hspace=0.05, wspace=0.1, figure=fig)

ax1 = fig.add_subplot(spec[0, 0], frameon=False)
removeTicks(ax1)

ax2 = fig.add_subplot(spec[1, 0], frameon=False)
removeTicks(ax2)

axin1 = ax2.inset_axes([0.0, 0.7, 0.30, 0.40], frameon=False)
removeTicks(axin1)

axin2 = ax2.inset_axes([0.35, 0.7, 0.30, 0.30], frameon=False)
removeTicks(axin2)

axin3 = ax2.inset_axes([0.70, 0.7, 0.30, 0.20], frameon=False)
removeTicks(axin3)

us = shp.Reader("tl_2017_us_state\\tl_2017_us_state.dbf")

nonmainlandus = ['Commonwealth of the Northern Mariana Islands', 'Guam', 'Puerto Rico', 'Hawaii', 'Alaska', 'American Samoa', 
                 'United States Virgin Islands']  

for shape in us.shapeRecords():
    
    if shape.record.NAME not in nonmainlandus:
        plotRegion(shape, ax1, [None, None])
 
    elif shape.record.NAME == 'Alaska':
        plotRegion(shape, axin1, [None, 100])

    elif shape.record.NAME == 'Hawaii':
        plotRegion(shape, axin2, [-162, None])

    elif shape.record.NAME == 'Puerto Rico':
        plotRegion(shape, axin3, [None, None])

plt.show()