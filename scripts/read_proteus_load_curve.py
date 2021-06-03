''' 
daniel vogler
2015

e.g.
python3 read_proteus_load_curve.py ~/projects/3d_printed_sstone/data/load_data/ ~/projects/3d_printed_sstone/figures/
'''

import csv
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import sys
import glob, os
import math
import warnings
import re
import matplotlib.colors as mcolors
import matplotlib.cm as cm

warnings.simplefilter("error")
#######

####### definitions

expRadius = 0.025

##################

print( "System input variables" )
print( str(sys.argv) )

# read in filepath from command line
filepath =  sys.argv[1]
figurePath =  sys.argv[2]

### Read in experimental data #########################

print( "Read experimental data" )
print( filepath )
print( "###########################################" )
print( "Processing experimental data" )


# define measurement locations on sample
testFiles = []

# find all files with given string
os.chdir(filepath)
variableName = "ethz_"
searchString = str(variableName+"*.txt")
print( "\t Searching test in path %s \n" %filepath )
#
for file in glob.glob(searchString):
	testFiles.append(file)
	print( "\t\t Found test file %s " %file )
print( "\n\t\t --> %d test files found for %s \n" %(len(testFiles), filepath) )
testFiles = sorted(testFiles)

# search string
expSearchString = 'Index'
expIndicesGlobal = [[] for _ in range(len(testFiles))]
# 
# maximum number of curves per file
maxTestsPerFile = 0
# 
# check number of tests in each file
print( "\n\n########################################\nReading number of tests in all files\n" )
for loadFileCounter in range(len(testFiles)):
	print( "\tReading test number in file %s" %testFiles[loadFileCounter] )
	fileToLoad = str(filepath+testFiles[loadFileCounter])
	with open(fileToLoad) as file:
	        expFile = csv.reader(file, delimiter=';', skipinitialspace=True)
	        for line in expFile:
	                expData = list(expFile)
	        #
			# find search string occurences in list
	        expIndices = [l for l, s in enumerate(expData) if str(expSearchString) in s]
	expIndicesGlobal[loadFileCounter] = expIndices
	# check maximum size of tests per file
	maxTestsPerFile = max(maxTestsPerFile, len(expIndicesGlobal[loadFileCounter])-1 )


# initialize variables
listExpIndex = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpElement = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpMarker = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpTime = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpForceDiff = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpMachineDisplacement = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpSensorDisplacement = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
listExpSigmaZ = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
# initialize variables
expIndex = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expElement = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expMarker = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expTime = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expForceDiff = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expMachineDisplacement = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
expSensorDisplacement = [ [ [] for _ in range(maxTestsPerFile)]for _ in range(len(testFiles))]
expSigmaZ = [ [ [] for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
#
# label of each test
expLabel = [ [ 0 for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
#
maxLoadIdx 	 = [ [ 0 for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
maxSigmaZIdx = [ [ 0 for _ in range(maxTestsPerFile)] for _ in range(len(testFiles))]
# mean and std sigma tensile
maxSigmaZ = [ [] for _ in range(len(testFiles))]
meanSigmaZ 	 = [ [] for _ in range(len(testFiles))]
stdSigmaZ = [ [] for _ in range(len(testFiles))]


# load all tests for each file
print( "\n\n########################################\nReading test data in all files\n" )
for loadFileCounter in range(len(testFiles)):
	print( "\tOpening file %s" %testFiles[loadFileCounter] )
	fileToLoad = str(filepath+testFiles[loadFileCounter])
	with open(fileToLoad) as file:
	        expFile = csv.reader(file, delimiter=';', skipinitialspace=True)
	        for line in expFile:
	                expData = list(expFile)
	        #
			# find search string occurences in list
	        expIndices = [l for l, s in enumerate(expData) if str(expSearchString) in s]

	for k in range( len( expIndicesGlobal[loadFileCounter] ) - 1):
		# save experiment label
		expLabel[loadFileCounter][k] = expData[expIndices[k]-2][0]
		# seperate data sheets
		for l in range(expIndices[k]+2, expIndices[k+1]-4):
			listExpIndex[loadFileCounter][k].append( float(expData[l][0]) )
			listExpElement[loadFileCounter][k].append( float(expData[l][1]) )
			listExpMarker[loadFileCounter][k].append( float(expData[l][2]) )
			listExpTime[loadFileCounter][k].append( expData[l][3]) 
			listExpForceDiff[loadFileCounter][k].append( float(expData[l][4]) )
			listExpMachineDisplacement[loadFileCounter][k].append( float(expData[l][5]) )
			#listExpSensorDisplacement[loadFileCounter][k].append( float(expData[l][6]) )
			listExpSigmaZ[loadFileCounter][k].append( float(expData[l][4])/(math.pi*expRadius**2) )


print( "\n\n##################################################\nMean and std of tensile stress during experiment:" )
# convert to array and print max results
for loadFileCounter in range(len(testFiles)):
	for k in range( len( expIndicesGlobal[loadFileCounter] ) - 1):
		expIndex[loadFileCounter][k] = np.array(listExpIndex[loadFileCounter][k]).astype(np.float)
		expForceDiff[loadFileCounter][k] = np.array(listExpForceDiff[loadFileCounter][k]).astype(np.float)
		expMachineDisplacement[loadFileCounter][k] = np.array(listExpMachineDisplacement[loadFileCounter][k]).astype(np.float)
		#expSensorDisplacement[loadFileCounter][k] = np.array(listExpSensorDisplacement[loadFileCounter]).astype(np.float)
		expSigmaZ[loadFileCounter][k] = expForceDiff[loadFileCounter][k]/(math.pi*expRadius**2)/1e3
		# find maximum load and stress indexes
		maxLoadIdx[loadFileCounter][k] = ( expForceDiff[loadFileCounter][k].argmax(axis=0) )
		maxSigmaZIdx[loadFileCounter][k] = ( expSigmaZ[loadFileCounter][k].argmax(axis=0) )
		#
		maxSigmaZ[loadFileCounter].append( expSigmaZ[loadFileCounter][k][maxSigmaZIdx[loadFileCounter][k]] )
		#
		'''
		print "Maximum force difference during experiment:"
		print "%s" %testFiles[loadFileCounter]
		print "%d" %k
		print "%3.2f [kN]" %expForceDiff[loadFileCounter][k][maxLoadIdx[loadFileCounter][k]]
		print "%3.2f [MPa]" %expSigmaZ[loadFileCounter][k][maxSigmaZIdx[loadFileCounter][k]]
		print 
		'''
	meanSigmaZ[loadFileCounter] = np.mean( maxSigmaZ[loadFileCounter] )
	stdSigmaZ[loadFileCounter] = np.std( maxSigmaZ[loadFileCounter] )
	#	
	print( "%s" %testFiles[loadFileCounter] )
	print( "Mean: %3.2f [MPa]" %meanSigmaZ[loadFileCounter] )
	print( " Std: %3.2f [MPa]" %stdSigmaZ[loadFileCounter] )

	

# formula for sigma tensile
# sigma_tensile = ( 2*PrimaryFailureLoad) / (pi * diameter * thickness) in [MPa]


print( "##############################################################" )
print( "Plotting Figures" )

# plots
# settings
markerSize = 10.0
lineStyle = 'none'
legendLocation = "upper left"
Color = ['b', 'r', 'm', 'g']
conversionFactor = 1000
fontSize = 20
# colormap
normalize = mcolors.Normalize( vmin=0.0, vmax=len(testFiles) )
colormap = cm.jet#cm.gnuplot

# plot - sigma tensile

for loadFileCounter in range(len(testFiles)):

	fig = pl.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
	# print data
	for k in range( len( expIndicesGlobal[loadFileCounter] ) - 1):
		pl.plot( k , expSigmaZ[loadFileCounter][k][maxSigmaZIdx[loadFileCounter][k]], color="black", marker='o', label=expLabel[loadFileCounter][k], markersize=markerSize, linestyle="none")

	# tick labels and limits
	pl.locator_params(nbins=4)
	xTickLabel = (expLabel[loadFileCounter][:])
	xTickRange = range( len( expIndicesGlobal[loadFileCounter] ) -1)
	while xTickLabel[-1] == 0:
        	xTickLabel.pop()
	pl.xlim([xTickRange[0]-1, xTickRange[-1]+1])
	pl.xticks( xTickRange, xTickLabel)
	pl.ylabel('sigma tensile [MPa]', fontsize = fontSize)
	pl.xlabel('test [-]', fontsize = fontSize)
	pl.tick_params(axis='both', which='major', labelsize=fontSize)
	# legend
	#pl.legend(loc=legendLocation, numpoints = 1,title="Cycle [-]")
	# save figure path
	saveString = re.sub("\.txt", "", testFiles[loadFileCounter])
	# save figures
	pl.savefig( str(figurePath+saveString+"_sigmaTensile_vs_tests.png"), bbox_inches='tight' )


pl.show()
exit()
