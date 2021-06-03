'''
daniel vogler
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import math
import sys
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.collections as mc
import random
import csv

import itertools
import time

## dd/mm/yyyy format
current_date =  (time.strftime("%Y%m%d"))
print("Current day - %s" %current_date)
##################

# labels
labels = ['Art. Coarse (GS19)', 'Art. Fine (GS14)', 'Buchs', 'Baerlauch', 'Massongex']
# define grain size variables
grain_size = [[] for x in range(7)]
grain_size_distribution = [[] for x in range(5)]
grain_size_distribution_cummulative = [[] for x in range(5)]


# intiialize counter
i = -1

# open file
import csv
with open('properties.txt', 'r') as f:
	reader = csv.reader(f, dialect='excel', delimiter='\t')
	for row in reader:
		i += 1
		grain_size[i][:] = row

# convert bin size to float
grain_size_bins = np.array( grain_size[1][1:] ).astype(np.float)

# convert grain size frequencies to float
for l in range(2,7):
	grain_size_distribution[l-2][:] = np.array( grain_size[l][1:] ).astype(np.float)

# plot pdf
pl.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')

# pick colorbar
colormap = cm.gnuplot
# plot size
font = {'size'   : 22}
pl.rc('font', **font)
pl.rcParams.update({'font.size': 22})

# normalize colorbar
normalize = mcolors.Normalize( vmin=0.0, vmax=5)

for l in range(5):
	print( "\t Plot histogram \n" )
	# sort color according to bins
	#pl.fill_between( grain_size_bins , 0, grain_size_distribution[l][:] , color= colormap( normalize(l) ) , linestyle='-', alpha=0.3)
	pl.plot( grain_size_bins , grain_size_distribution[l][:]/sum(grain_size_distribution[l][:]) , linewidth=4.0, color=colormap( normalize(l) ) , linestyle='-')
	pl.plot([], [], label=labels[l], color=colormap( normalize(l) ), linewidth=4.0 )

pl.xlabel("grain size [$\mu m$]")
pl.ylabel("frequency [-]")
pl.legend(loc='upper right', numpoints = 1)
pl.xlim([0.0, 800])
pl.savefig( str( "./ethz_sandstone_grain_size_distribution.png"), bbox_inches='tight' )

# plot cumulative distribution
pl.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')

# pick colorbar
colormap = cm.gnuplot
# plot size
font = {'size'   : 22}
pl.rc('font', **font)
pl.rcParams.update({'font.size': 22})

# normalize colorbar
normalize = mcolors.Normalize( vmin=0.0, vmax=5)

print( np.size( grain_size_distribution[l][:] ) )
print( np.size( grain_size_distribution_cummulative[l][:] ) )


for l in range(5):
	print("\t Plot histogram \n")
	# sort color according to bins
	#pl.fill_between( grain_size_bins , 0, grain_size_distribution[l][:] , color= colormap( normalize(l) ) , linestyle='-', alpha=0.3)
	grain_size_distribution_cummulative[l].append(0.0)
	for k in range(np.size(grain_size_distribution[l][:])-1):
		grain_size_distribution_cummulative[l].append(grain_size_distribution_cummulative[l][k] + grain_size_distribution[l][k+1])

	pl.plot( grain_size_bins , grain_size_distribution_cummulative[l][:]/grain_size_distribution_cummulative[l][-1]*100 , linewidth=4.0, color=colormap( normalize(l) ) , linestyle='-')
	pl.plot([], [], label=labels[l], color=colormap( normalize(l) ), linewidth=4.0 )



pl.xlabel("Grain size [$\mu m$]")
pl.ylabel("Percent [-]")
pl.legend(loc='lower right', numpoints = 1)
pl.xlim([0.0, 600])
pl.savefig( str( "./ethz_sandstone_grain_size_distribution_cummulative.png"), bbox_inches='tight' )


pl.show()
exit()
